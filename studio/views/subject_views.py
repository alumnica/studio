from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, FormView
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
        tags = self.request.POST.get('tags-materias').split(',')
        subject = form.save_form(self.request.user, tags)
        return redirect(to='materias_sections_view', subject_name=subject.name)

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all()
        return render(self.request, self.template_name, {'form': form, 'subjects': subjects, 'tags': tags})


class SubjectSectionsView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    form_class = SubjectSectionsForm
    template_name = 'studio/pages/test.html'

    def form_valid(self, form):
        subject_name = self.kwargs.get('subject_name', None)
        subject = SubjectModel.objects.get(name_field=subject_name)
        section = 1
        section_images = self.request.FILES.items()
        form.save_form(section_images, subject)
        return redirect(to='odas_section_view', section=section, subject_name=subject_name)


class ODAsSectionView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    form_class = ODAsSectionForm
    template_name = 'studio/pages/test.html'

    def get(self, request, *args, **kwargs):
        subject_name = self.kwargs.get('subject_name', None)
        section = int(self.kwargs.get('section', None))

        subject = SubjectModel.objects.get(name_field=subject_name)

        if section <= subject.number_of_sections:
            section_img = subject.sections_images[section]
            form = ODAsSectionForm(initial={'section_field': section, 'subject_field': subject_name, 'odas_counter': 8})
            return render(request, self.template_name, {'form': form, 'section_img': section_img})
        else:
            return redirect(to='materias_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors.items[0], persistent='Ok')
        return render(self.request, self.template_name, {'form': form})

    def form_valid(self, form):
        subject_name = self.kwargs.get('subject_name', None)
        section = int(self.kwargs.get('section', None))

        names_list = []
        images_list = self.request.FILES.items()
        number_images = self.request.FILES.__len__()
        for i in range(1, number_images):
            names_list.extend(self.request.POST.get('oda_name%s' % i))

        subject = form.save_form(self.request.user, subject_name, names_list, images_list, section)

        if section == subject.number_of_sections:
            return redirect(to='materias_view')
        else:
            section += 1
            return redirect(to='odas_section_view', section=section, subject_name=subject_name)


class SubjectView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias.html'
    queryset = SubjectModel.objects.all()
    context_object_name = 'subject_list'
