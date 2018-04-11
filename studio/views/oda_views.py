from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView
from sweetify import sweetify
from studio.forms.oda_forms import *


class ODAsSectionView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    form_class = ODAsSectionForm
    template_name = 'studio/pages/test.html'

    def get(self, request, *args, **kwargs):
        subject_name = self.kwargs.get('subject_name', None)
        section = int(self.kwargs.get('section', None))
        subject = SubjectModel.objects.get(name_field=subject_name)

        if section <= 0:
            return redirect(to='materias_view')

        if section <= subject.number_of_sections:
            section_img = subject.sections_images[section-1]
            form = ODAsSectionForm(initial={'section_field': section, 'subject_field': subject_name, 'odas_counter': 8})
            return render(request, self.template_name, {'form': form, 'section_img': section_img})
        else:
            return redirect(to='materias_view')

    def form_invalid(self, form):
        if form['section_field'].errors:
            sweetify.error(self.request, form.errors['section_field'][0], persistent='Ok')
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


class ODAsPositionView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    form_class = ODAsPositionForm
    template_name = 'studio/pages/test.html'

    def get(self, request, *args, **kwargs):
        subject_name = self.kwargs.get('subject_name', None)
        section = int(self.kwargs.get('section', None))
        subject = SubjectModel.objects.get(name_field=subject_name)

        if section <= 0:
            return redirect(to='materias_view')

        if section <= subject.number_of_sections:
            section_img = subject.sections_images[section-1]
            form = ODAsPositionForm(initial={'section_field': section, 'subject_field': subject_name})
            return render(request, self.template_name, {'form': form, 'section_img': section_img, 'odas': subject.odas})
        else:
            return redirect(to='materias_view')

