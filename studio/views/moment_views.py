from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import Moment, Tag
from alumnica_model.models.content import MomentType, Subject
from studio.forms.moment_forms import MomentCreateForm, MomentUpdateForm
from studio_webapp.settings import AWS_INSTANCE_URL


class MomentsView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    Momentos dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    queryset = Moment.objects.all()
    context_object_name = 'moments_list'


class CreateMomentView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, CreateView):
    """
    Create new Momento object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
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

            if subject.ambit is not None:
                if not subject.ambit.is_draft:
                    continue

            for oda in subject.odas.all():
                microodas = []
                for microoda in oda.microodas.all():
                    if microoda.activities.all().count() < 3:
                        microodas.append(microoda.type.name)

                if len(microodas) > 0:
                    odas.append(oda)
                    microodas_list.append(microodas)
            if len(odas) > 0:
                odas_zip = zip(odas, microodas_list)
                odas_list.append(odas_zip)
                subjects_list.append(subject)

        subject_odas = zip(subjects_list, odas_list)

        context = super(CreateMomentView, self).get_context_data(**kwargs)
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
        h5p_job_id = self.request.POST.get('url_h5p')
        form.save_form(self.request.user, subject, oda, microoda, moment_type, h5p_job_id)
        return redirect(to='momentos_view')


class UpdateMomentView(LoginRequiredMixin, UpdateView):
    """
    Update existing Momento view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos-edit.html'
    form_class = MomentUpdateForm

    def get_object(self, queryset=None):
        return Moment.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        moment_type_list = MomentType.objects.all()
        subjects_list = []
        odas_list = []

        for subject in Subject.objects.all():
            odas = []
            microodas_list = []

            if subject.ambit is not None:
                if self.object.microoda is not None:
                    if not subject.ambit.is_draft and self.object.microoda.oda.subject != subject:
                        continue

            for oda in subject.odas.all():
                microodas = []
                for microoda in oda.microodas.all():
                    if microoda.activities.all().count() < 3 or microoda != self.object.microoda:
                        microodas.append(microoda.type.name)

                if len(microodas) > 0:
                    odas.append(oda)
                    microodas_list.append(microodas)
            if len(odas) > 0:
                odas_zip = zip(odas, microodas_list)
                odas_list.append(odas_zip)
                subjects_list.append(subject)

        subject_odas = zip(subjects_list, odas_list)

        context = super(UpdateMomentView, self).get_context_data(**kwargs)
        context.update({'moments_list': moments_list,
                        'tags': tags,
                        'subject_odas': subject_odas,
                        'moment_type_list': moment_type_list,
                        "aws_url": AWS_INSTANCE_URL})
        return context

    def form_valid(self, form):
        subject = self.request.POST.get('materia-list')
        oda = self.request.POST.get('oda-list')
        microoda = self.request.POST.get('micro-oda')
        moment_type = self.request.POST.get('tipo-momento')
        h5p_url = self.request.POST.get('url_h5p')
        form.save_form(subject, oda, microoda, moment_type, h5p_url)
        return redirect(to='momentos_view')


class DeleteMomentView(View):
    """
    Deletes Momento object
    """
    def dispatch(self, request, *args, **kwargs):
        Moment.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect(to='momentos_view')
