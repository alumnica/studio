from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from sweetify import sweetify
from studio.forms.subject_forms import *


class CreateSubjectView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit.html'
    form_class = SubjectForm

    def get_image_formset_class(self):
        return formset_factory(
            ImageModelForm,
            BaseImageModelFormset,
            min_num=1,
            max_num=1,
            validate_max=False,
            validate_min=True,
        )

    def get_context_data(self, **kwargs):
        context = super(CreateSubjectView, self).get_context_data(**kwargs)
        tags = TagModel.objects.all()
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

        subject = form.save_form(self.request.user, action == 'save')
        formset = context['formset']
        section = 1
        formset_count = 0
        if formset.is_valid():
            if formset.has_changed():
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file_field):
                        a.name_field = '{}-subject_section_image'.format(subject.name)
                        a.folder_field = "subjects"
                        a.file_name_field = os.path.basename(a.file_field.name)
                        a.save()
                        section += 1
                        subject.sections_images_field.add(a)
                        formset_count += 1
                subject.number_of_sections_field = formset_count
                subject.save()
        else:
            i = 1
            for form in formset:
                if form['file_field'].errors:
                    sweetify.error(
                        self.request,
                        "Error en archivo de imagen de la sección {}: {}".format(i, form.errors['file_field'][0]),
                        persistent='Ok')
                    break
                i += 1
            return render(self.request, self.template_name, context=context)

        if action == 'save':
            return redirect(to='materias_view')
        else:
            return redirect(to='odas_section_view', pk=subject.pk, section=1)

    def form_invalid(self, form):

        if form['name_field'].errors:
            sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        if form['mp'].errors:
            sweetify.error(self.request, form.errors['mp'][0], persistent='Ok')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class UpdateSubjectView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit.html'
    model = SubjectModel
    form_class = UpdateSubjectForm

    def get_image_formset_class(self):
        num_sections = self.object.number_of_sections_field
        if num_sections == 0:
            num_sections = 1
        return formset_factory(
            ImageModelForm,
            BaseImageModelFormset,
            min_num=num_sections,
            max_num=self.object.number_of_sections_field,
            validate_max=False,
            validate_min=False,
            can_delete=True)

    def get_context_data(self, **kwargs):
        context = super(UpdateSubjectView, self).get_context_data(**kwargs)
        ambits = AmbitModel.objects.all()
        tags = TagModel.objects.all()
        tgs = self.object.tags_field.all()
        background_img = self.object.background_image_field

        initial = [{'file_field': x.file_field} for x in self.object.sections_images_field.all()]
        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial,
                                                          form_instances=[
                                                              x for x in self.object.sections_images_field.all()
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
        if form['name_field'].errors:
            sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        if form['mp'].errors:
            sweetify.error(self.request, form.errors['mp'][0], persistent='Ok')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)

    def form_valid(self, form):
        context = self.get_context_data()

        action = self.request.POST.get('action')
        subject = form.save_form(action == 'save')

        formset = context['formset']
        section = 1
        formset_count = len(formset)
        current_sections = []
        if formset.is_valid():
            if formset.has_changed():
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file_field):
                        a.name_field = '{}-subject_section_image'.format(subject.name)
                        a.folder_field = "subjects"
                        a.file_name_field = os.path.basename(a.file_field.name)
                        a.save()
                        section += 1
                        current_sections.append(a.pk)
                        if a not in self.object.sections_images_field.all():
                            self.object.sections_images_field.add(a)
            else:
                for form in formset:
                    a = form.save(commit=False)
                    if bool(a.file_field):
                        current_sections.append(a.pk)

            subject.number_of_sections_field = formset_count

            for deleted_form in formset.deleted_forms:
                object_to_delete = deleted_form.save(commit=False)
                object_to_delete.delete()
                subject.number_of_sections_field -= 1

            subject.save()

            self.object.save()
            self.object.update_sections(current_sections)
        else:
            i = 1
            for form in formset:
                if form['file_field'].errors:
                    sweetify.error(
                        self.request,
                        "Error en archivo de imagen de la sección {}: {}".format(i, form.errors['file_field'][0]),
                        persistent='Ok')
                    break
                i += 1
            return render(self.request, self.template_name, context=context)

        if action == 'save':
            return redirect(to='materias_view')
        else:
            return redirect(to='odas_section_view', pk=subject.pk, section=1)


class SubjectView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias.html'
    queryset = SubjectModel.objects.all()
    context_object_name = 'subject_list'


class DeleteSubjectView(View):
    def dispatch(self, request, *args, **kwargs):
        SubjectModel.objects.filter(pk=self.kwargs['pk']).delete()
        return redirect('materias_view')
