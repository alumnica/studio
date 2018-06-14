from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from alumnica_model.models import Moment, Tag, ODA
from alumnica_model.models.content import MomentType, Subject
from studio.forms.moment_forms import MomentCreateForm


class MomentsView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    form_class = MomentCreateForm

    def get_context_data(self, **kwargs):
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        moment_type_list = MomentType.objects.all()
        subjects_list = []
        odas_list = []

        for subject in Subject.objects.all():
            odas = []
            microodas_list = []
            for oda in subject.odas.all():
                microodas = []
                for microoda in oda.microodas.all():
                    if microoda.activities.all().count() < 3:
                        microodas.append(microoda.type)

                if len(microodas) > 0:
                    odas.append(oda)
                    microodas_list.append(microodas)
            if len(odas) > 0:
                odas_zip = zip(odas, microodas_list)
                odas_list.append(odas_zip)
                subjects_list.append(subject)

        subject_odas = zip(subjects_list, odas_list)

        context = super(MomentsView, self).get_context_data(**kwargs)
        context.update({'moments_list': moments_list,
                        'tags': tags,
                        'subject_odas': subject_odas,
                        'moment_type_list': moment_type_list})
        return context

    def form_valid(self, form):
        subject = self.request.POST.get('materia-list')
        oda = self.request.POST.get('oda-list')
        microoda = self.request.POST.get('micro-oda')
        moment_type = self.request.POST.get('tipo-momento')
        h5p_url = self.request.POST.get('url_h5p')
        form.save_form(self.request.user, subject, oda, microoda, moment_type, h5p_url)
        return redirect(to='momentos_view')