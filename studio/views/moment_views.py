from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from alumnica_model.models import Moment, Tag, ODA
from alumnica_model.models.content import MomentType
from studio.forms.moment_forms import MomentCreateForm


class MomentsView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    form_class = MomentCreateForm

    def get_context_data(self, **kwargs):
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        moment_type_list = MomentType.objects.all()
        odas_list = []

        microodas_list = []

        for oda in ODA.objects.filter():
            microodas = []
            for microoda in oda.microodas.all():
                if microoda.activities.all().count() < 3:
                    microodas.append(microoda.type)
            if len(microodas) > 0:
                odas_list.append(oda)
                microodas_list.append(microodas)

        odas_microodas = zip(odas_list, microodas_list)

        context = super(MomentsView, self).get_context_data(**kwargs)
        context.update({'moments_list': moments_list,
                        'tags': tags,
                        'odas_microodas': odas_microodas,
                        'moment_type_list': moment_type_list})
        return context

    def form_valid(self, form):
        oda = self.request.POST.get('oda-list')
        microoda = self.request.POST.get('micro-oda')
        moment_type = self.request.POST.get('tipo-momento')
        form.save_form(self.request.user, oda, microoda, moment_type)
        return redirect(to='momentos_view')