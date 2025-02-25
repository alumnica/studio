import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import Tag, Subject, Ambit, users
from studio.forms.subject_forms import SubjectForm, BaseImageFormset, ImageForm, UpdateSubjectForm


class CreateSubjectView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, CreateView):
    """
    Create new Subject object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit.html'
    form_class = SubjectForm

    def get_image_formset_class(self):
        return formset_factory(
            ImageForm,
            BaseImageFormset,
            min_num=1,
            max_num=1,
            validate_max=False,
            validate_min=True,
        )

    def get_context_data(self, **kwargs):
        context = super(CreateSubjectView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        initial = [{'initial': 'initial'}]
        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial),
                'tags': tags
            })
        else:
            context.update({
                'formset': self.get_image_formset_class()(initial=initial),
                'tags': tags
            })

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        action = self.request.POST.get('action')

        subject, finalized = form.save_form(self.request.user, action == 'save')
        formset = context['formset']
        section = 1
        formset_count = 0
        if formset.is_valid():
            if formset.has_changed():
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file):
                        a.name = '{}-subject_section_image'.format(subject.name)
                        a.folder = "subjects"
                        a.file_name = os.path.basename(a.file.name)
                        a.save()
                        section += 1
                        subject.sections_images.add(a)
                        formset_count += 1
                subject.number_of_sections = formset_count
                subject.save()
        else:
            i = 1
            for form in formset:
                if form['file'].errors:
                    sweetify.error(
                        self.request,
                        'Error en la imagen de la sección {} '.format(i, form.errors['file'][0]), persistent='Ok')
                    break
                i += 1
            return render(self.request, self.template_name, context=context)

        if action == 'save' or action == 'eva-publish':
            if action == 'eva-publish' and not finalized:
                sweetify.error(
                    self.request,
                    "Coloca un ODA antes de finalizar",
                    persistent='Ok'
                )
                return redirect('update_subject_view', pk=subject.pk)
            return redirect(to='materias_view')
        else:
            action_array = action.split('-')
            section = int(action_array[(len(action_array) - 1)])
            return redirect(to='odas_position_view', pk=subject.pk, section=(section + 1))

    def form_invalid(self, form):
        if form['name'].errors:
            sweetify.error(self.request, form.errors['name'][0], persistent='Ok')
        elif form['mp'].errors:
            sweetify.error(self.request, form.errors['mp'][0], persistent='Ok')
        elif form['tags'].errors:
            sweetify.error(self.request, 'Error en el campo de tags: {}'.format(form.errors['tags'][0]),
                           persistent='OK')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class UpdateSubjectView(LoginRequiredMixin, UpdateView):
    """
    Update existing Subject view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit.html'
    model = Subject
    form_class = UpdateSubjectForm

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        if subject.ambit is not None:
            if subject.ambit.is_published:
                if self.request.user.user_type == users.TYPE_CONTENT_CREATOR:
                    sweetify.error(
                        self.request,
                        'No puedes editar la materia {} porque pertenece a un ámbito publicado'.format(
                            subject.name),
                        persistent='Ok')
                    return redirect(to='materias_view')
        return super(UpdateSubjectView, self).dispatch(request, *args, **kwargs)

    def get_image_formset_class(self):
        num_sections = self.object.number_of_sections
        if num_sections == 0:
            num_sections = 1
        return formset_factory(
            ImageForm,
            BaseImageFormset,
            min_num=num_sections,
            max_num=self.object.number_of_sections,
            validate_max=False,
            validate_min=False,
            can_delete=True)

    def get_context_data(self, **kwargs):
        context = super(UpdateSubjectView, self).get_context_data(**kwargs)
        ambits = Ambit.objects.all()
        tags = Tag.objects.all()
        tgs = self.object.tags.all()
        background_img = self.object.background_image

        initial = [{'file': x.file} for x in self.object.sections_images.all()]
        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial,
                                                          form_instances=[
                                                              x for x in self.object.sections_images.all()
                                                          ])
            })
        else:
            context.update({
                'formset': self.get_image_formset_class()(initial=initial),
                'tags': tags,
                'ambits': ambits,
                'self_tags': tgs,
                'background_img': background_img
            })
        return context

    def form_invalid(self, form):
        if form['name'].errors:
            sweetify.error(self.request, form.errors['name'][0], persistent='Ok')
        elif form['mp'].errors:
            sweetify.error(self.request, form.errors['mp'][0], persistent='Ok')
        elif form['tags'].errors:
            sweetify.error(self.request, 'Error en el campo de tags: {}'.format(form.errors['tags'][0]),
                           persistent='OK')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)

    def form_valid(self, form):
        context = self.get_context_data()

        action = self.request.POST.get('action')
        subject, finalized = form.save_form(action == 'save')

        formset = context['formset']
        section = 1
        formset_count = len(formset)
        current_sections = []
        if formset.is_valid():
            if formset.has_changed():
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file):
                        a.name = '{}-subject_section_image'.format(subject.name)
                        a.folder = "subjects"
                        a.file_name = os.path.basename(a.file.name)
                        a.save()
                        section += 1
                        current_sections.append(a.pk)
                        if a not in self.object.sections_images.all():
                            self.object.sections_images.add(a)
            else:
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file):
                        current_sections.append(a.pk)

            subject.number_of_sections = formset_count

            for deleted_form in formset.deleted_forms:
                object_to_delete = deleted_form.save(commit=False)
                if object_to_delete in subject.sections_images.all():
                    object_to_delete.delete()
                subject.number_of_sections -= 1

            subject.save()

            self.object.save()
            self.object.update_sections(current_sections)
        else:
            i = 1
            for form in formset:
                if form['file'].errors:
                    sweetify.error(
                        self.request,
                        "Error en el archivo de la sección {}: {}".format(i, form.errors['file'][0]),
                        persistent='Ok'
                    )
                    break
                i += 1
            return render(self.request, self.template_name, context=context)

        if action == 'save' or action == 'eva-publish':
            if action == 'eva-publish' and not finalized:
                sweetify.error(
                    self.request,
                    "Coloca un ODA antes de finalizar",
                    persistent='Ok'
                )
                return redirect('update_subject_view', pk=subject.pk)
            return redirect(to='materias_view')
        else:
            action_array = action.split('-')
            section = int(action_array[(len(action_array) - 1)])
            return redirect(to='odas_position_view', pk=subject.pk, section=(section + 1))


class SubjectView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    Subjects dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias.html'
    queryset = Subject.objects.all()
    context_object_name = 'subject_list'


class DeleteSubjectView(View):
    """
    Deletes Subject object
    """

    def dispatch(self, request, *args, **kwargs):
        Subject.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect('materias_view')
