from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView
from sweetify import sweetify
from studio.forms.oda_forms import *


class ODAsSectionView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit-oda.html'
    #template_name = 'studio/pages/odasTest.html'
    model = SubjectModel
    fields = ['name_field']

    def get_success_url(self):
        section = self.kwargs['section']
        if self.object.number_of_sections_field > section:
            section += 1
            return reverse_lazy('odas_section_view', kwargs={'pk': self.kwargs['pk'], 'section': section})

        else:
            return redirect(to='positions_view')

    def get_image_formset_class(self):
        section = self.kwargs['section']
        num_odas = self.object.odas_field.all().filter(section_field=section).count()
        if num_odas == 0:
            num_odas = 1
        return formset_factory(
            ODAModelForm, BaseODAModelFormset, min_num=num_odas, max_num=num_odas, validate_max=False,
            validate_min=True)

    def get_context_data(self, **kwargs):
        section = self.kwargs['section']
        background_image = self.object.sections_images_field.all()[section-1]
        odas_list = ODAModel.objects.all()
        context = super(ODAsSectionView, self).get_context_data(**kwargs)
        initial = [{'oda_field': x.oda_field, 'active_icon_field': x.active_icon_field,
                    'completed_icon_field': x.completed_icon_field} for x in
                   self.object.odas_field.all().filter(section_field=section)]

        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial,
                                                          form_instances=[
                                                              x for x in
                                                              self.object.odas_field.all().filter(section_field=section)
                                                          ]),
                'background_image': background_image
            })
        else:

            context.update({
                'formset': self.get_image_formset_class()(initial=initial),
                'background_image': background_image,
                'odas_list': odas_list
            })
        return context

    def form_valid(self, form):
        section = self.kwargs['section']
        formset = self.get_context_data()['formset']
        if formset.is_valid() and formset.has_changed():
            for form in formset:
                a = form.save(commit=False)
                a.section_field = section
                a.save()
                if a not in self.object.odas_field.all().filter(section_field=section):
                    self.object.odas_field.add(a)
            self.object.save()
        return super(ODAsSectionView, self).form_valid(form)


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

