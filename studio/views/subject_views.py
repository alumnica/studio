from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView
from sweetify import sweetify

from alumnica_model.models import AmbitModel
from studio.forms.subject_forms import *


class CreateSubjectView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit.html'
    form_class = CreateSubjectForm

    def get(self, request, *args, **kwargs):
        ambits = AmbitModel.objects.all()
        tags = TagModel.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'ambit': ambits, 'tags': tags})

    def form_valid(self, form):
        #image = self.request.FILES['image_file']
        #subject = form.save_form(self.request.user, image)
        subject = form.save_form(self.request.user)
        return redirect(to='materias_sections_view', pk=subject.pk)

    def form_invalid(self, form):
        if form['name_field'].errors:
            sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all()
        return render(self.request, self.template_name, {'form': form, 'subjects': subjects, 'tags': tags})


class SubjectSectionsView(UpdateView):
    model = SubjectModel
    fields = ['name_field', 'number_of_sections_field']
    template_name = 'studio/pages/testSections.html'
    context_object_name = 'subject'

    def get_success_url(self):
        return reverse_lazy('materias_sections_view', kwargs={'pk': self.kwargs['pk']})

    def get_image_formset_class(self):
        return formset_factory(
            ImageModelForm, BaseImageModelFormset, min_num=self.object.number_of_sections_field,
            max_num=self.object.number_of_sections_field,
            validate_max=False, validate_min=True
        )

    def get_context_data(self, **kwargs):
        context = super(SubjectSectionsView, self).get_context_data(**kwargs)
        initial = [{'name_field': x.name_field, 'file_field': x.file_field} for x in self.object.sections_images_field.all()]

        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial,
                                                          form_instances=[
                                                              x for x in self.object.sections_images_field.all()
                                                          ])
            })
        else:
            context.update({
                'formset': self.get_image_formset_class()(initial=initial)
            })

        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid() and formset.has_changed():
            for form in formset:
                a = form.save()
                if a not in self.object.sections_images_field.all():
                    self.object.sections_images_field.add(a)
            self.object.save()
        return super(SubjectSectionsView, self).form_valid(form)


class SubjectView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias.html'
    queryset = SubjectModel.objects.all()
    context_object_name = 'subject_list'
