from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import FormView, UpdateView, ListView, CreateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import Subject, ODA, Tag, Moment, users
from alumnica_model.models.content import Evaluation, MicroODAType
from studio.forms.oda_forms import ODAsPositionForm, ODACreateForm, \
    ODAUpdateForm


class ODAsPositionView(LoginRequiredMixin, FormView):
    """
    Update ODA position view
    """
    login_url = 'login_view'
    form_class = ODAsPositionForm
    template_name = 'studio/dashboard/materias-edit-position.html'

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=kwargs['pk'])
        if len(subject.sections_images.all()) == 0:
            sweetify.error(
                self.request,
                _('It is not possible to position ODAs. Assign an image to a section first'),
                persistent='Ok')
            return redirect(to='update_subject_view', pk=self.kwargs['pk'])
        return super(ODAsPositionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        section = self.kwargs['section']
        pk = self.kwargs['pk']
        context = super(ODAsPositionView, self).get_context_data(**kwargs)
        context.update({'pk': pk, 'section': section})
        return context

    def get(self, request, *args, **kwargs):
        section = self.kwargs['section']
        subject = Subject.objects.get(pk=self.kwargs['pk'])

        if section <= 0:
            return redirect(to='update_subject_view', pk=subject.pk)
        context = self.get_context_data()
        if section <= subject.number_of_sections:
            section_img = subject.sections_images.all()[section - 1]
            form = ODAsPositionForm(initial={'name': subject.name})
            odas_list = subject.odas.filter(section=section, temporal=False)
            context.update({'form': form, 'section_img': section_img, 'odas_list': odas_list})
            return render(request, self.template_name, context=context)
        else:
            return redirect(to='update_subject_view', pk=subject.pk)

    def form_valid(self, form):
        section = self.kwargs['section']
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        odas_to_save = subject.odas.filter(section=section)

        odas_position = self.request.POST.get('oda-position').split(';')

        for oda_info in odas_position:
            oda_data = oda_info.split(',')
            oda = odas_to_save.get(pk=int(oda_data[0]))
            oda.zone = oda_data[1].split('-')[1]
            oda.save()

        section += 1

        return redirect(to='update_subject_view', pk=subject.pk)


class ODADashboardView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    ODA dashboard view
    """
    login_url = 'login_view'
    model = ODA
    template_name = 'studio/dashboard/odas.html'
    queryset = ODA.objects.all()
    context_object_name = 'odas_list'


class ODACreateView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, CreateView):
    """
    Create new ODA view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/odas-edit.html'
    form_class = ODACreateForm

    def get(self, request, *args, **kwargs):
        tags_list = Tag.objects.all()
        moments_list = Moment.objects.filter(microoda=None)
        subjects_list = []

        bloques_list = []

        for subject in Subject.objects.filter(temporal=True):
            bloques = []
            if subject.ambit is not None:
                if not subject.ambit.is_draft:
                    continue
            for section in range(1, subject.number_of_sections + 1):
                if len(subject.odas.filter(section=section)) < 8:
                    bloques.append(section)
            if len(bloques) > 0:
                subjects_list.append(subject)
                bloques_list.append(bloques)

        subjects_sections = zip(subjects_list, bloques_list)
        eval_list = Evaluation.objects.filter(oda=None)

        return render(request, self.template_name,
                      {'form': self.form_class, 'tags_list': tags_list, 'moments_list': moments_list,
                       'subjects_sections': subjects_sections, 'eval_list': eval_list})

    def form_valid(self, form):
        moments = []

        application = self.request.POST.get('apli-momentos')
        template = ['application', application]
        moments.append(template)

        formalization = self.request.POST.get('forma-momentos')
        template = ['formalization', formalization]
        moments.append(template)

        activation = self.request.POST.get('activ-momentos')
        template = ['activation', activation]
        moments.append(template)

        exemplification = self.request.POST.get('ejem-momentos')
        template = ['exemplification', exemplification]
        moments.append(template)

        sensitization = self.request.POST.get('sens-momentos')
        template = ['sensitization', sensitization]
        moments.append(template)

        subject = self.request.POST.get('materia-a-oda')
        bloque = self.request.POST.get('bloque-a-oda')

        is_draft = True
        action = self.request.POST.get('action')
        if action == 'finalize':
            is_draft = False

        oda = form.save_form(self.request.user, moments, subject, bloque, is_draft)
        if action == 'edit_position':
            return redirect('odas_position_view', pk=oda.subject.pk, section=oda.section)
        return redirect(to='oda_dashboard_view')


class ODAUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update existing ODA object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/odas-edit.html'
    form_class = ODAUpdateForm

    def dispatch(self, request, *args, **kwargs):
        oda = ODA.objects.get(pk=self.kwargs['pk'])
        if oda.subject is not None:
            if oda.subject.ambit is not None:
                if oda.subject.ambit.is_published:
                    if self.request.user.user_type == users.TYPE_CONTENT_CREATOR:
                        sweetify.error(
                            self.request,
                            _('It is not possible to edit oda {} because it belongs to a published ambit'.format(
                                oda.name)),
                            persistent='Ok')
                        return redirect(to='oda_dashboard_view')
        return super(ODAUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return ODA.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ODAUpdateView, self).get_context_data(**kwargs)
        tags_list = Tag.objects.all()
        moments_list = Moment.objects.filter(microoda=None)
        self_tags = self.object.tags.all()

        apli_list = self.object.microodas.filter(type=MicroODAType.objects.get(name='application'))
        forma_list = self.object.microodas.filter(type=MicroODAType.objects.get(name='formalization'))
        activ_list = self.object.microodas.filter(type=MicroODAType.objects.get(name='activation'))
        ejem_list = self.object.microodas.filter(type=MicroODAType.objects.get(name='exemplification'))
        sens_list = self.object.microodas.filter(type=MicroODAType.objects.get(name='sensitization'))
        eval_list = Evaluation.objects.filter(oda=None)

        subjects_list = []
        bloques_list = []

        for subject in Subject.objects.filter():
            bloques = []

            if self.object.subject != subject:
                if subject.ambit is not None:
                    if not subject.ambit.is_draft and not subject.temporal:
                        continue
            for section in range(1, subject.number_of_sections + 1):
                if len(subject.odas.filter(section=section)) < 8:
                    bloques.append(section)
                else:
                    if self.object.subworld == subject and self.object.section == section:
                        bloques.append(section)
            if len(bloques) > 0:
                subjects_list.append(subject)
                bloques_list.append(bloques)

        subjects_sections = zip(subjects_list, bloques_list)

        context.update(
            {'subjects_sections': subjects_sections, 'tags_list': tags_list, 'moments_list': moments_list,
             'self_tags': self_tags, 'apli_list': apli_list, 'forma_list': forma_list,
             'activ_list': activ_list, 'ejem_list': ejem_list,
             'sens_list': sens_list, 'eval_list': eval_list})
        return context

    def form_valid(self, form):
        moments = []

        aplication = self.request.POST.get('apli-momentos')
        template = ['application', aplication]
        moments.append(template)

        formalization = self.request.POST.get('forma-momentos')
        template = ['formalization', formalization]
        moments.append(template)

        activation = self.request.POST.get('activ-momentos')
        template = ['activation', activation]
        moments.append(template)

        exemplification = self.request.POST.get('ejem-momentos')
        template = ['exemplification', exemplification]
        moments.append(template)

        sensitization = self.request.POST.get('sens-momentos')
        template = ['sensitization', sensitization]
        moments.append(template)

        evaluation = self.request.POST.get('eval-momentos')

        subject = self.request.POST.get('materia-a-oda')
        bloque = self.request.POST.get('bloque-a-oda')

        is_draft = True
        action = self.request.POST.get('action')
        if action != 'save':
            is_draft = False

        oda = form.save_form(self.request.user, moments, subject, bloque, evaluation, is_draft)
        if action == 'edit_position':
            return redirect('odas_position_view', pk=oda.subject.pk, section=oda.section)
        return redirect(to='oda_dashboard_view')


class ODAsRedirect(View):
    """
    Redirect to previous page view, depending on actual view name
    """
    def dispatch(self, request, *args, **kwargs):
        view = kwargs.get('view')
        section = kwargs.get('section')
        pk = kwargs.get('pk')
        if view == 'odas_preview_view':
            return redirect(to='odas_position_view', pk=pk,
                            section=Subject.objects.get(pk=pk).number_of_sections)

        if section == 1:
            if view == 'odas_section_view':
                return redirect(to='materias_sections_view', pk=pk)
            if view == 'odas_position_view':
                return redirect(to='odas_section_view', pk=pk,
                                section=Subject.objects.get(pk=pk).number_of_sections)
        else:
            return redirect(view, pk=pk, section=(kwargs.get('section') - 1))


class DeleteODAView(View):
    """
    Deletes ODA object
    """
    def dispatch(self, request, *args, **kwargs):
        ODA.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect('oda_dashboard_view')

