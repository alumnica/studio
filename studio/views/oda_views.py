from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, ListView, CreateView
from sweetify import sweetify

from alumnica_model.models import TagModel
from studio.forms.oda_forms import *


class ODAsSectionView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit-oda.html'
    form_class = ODAsSectionView

    def get_object(self, queryset=None):
        return SubjectModel.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        section = self.kwargs['section']
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])
        if subject.number_of_sections_field > section:
            section += 1
            return reverse_lazy('odas_section_view', kwargs={'pk': self.kwargs['pk'], 'section': section})

        else:
            return reverse_lazy('odas_position_view', kwargs={'pk': self.kwargs['pk'], 'section': 1})

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
        odas_list = []
        odas_to_avoid_list = []
        for oda in ODAModel.objects.all():
            odas_in_subject = oda.subject
            if len(odas_in_subject) == 0:
                odas_list.append(oda)
            else:
                for oda_in_subject in odas_in_subject:
                    if oda_in_subject.subject.all().filter(pk=self.kwargs['pk']).exists:
                        if oda_in_subject.section_field == section:
                            odas_list.append(oda)
                        else:
                            odas_to_avoid_list.append(oda)
                    else:
                        odas_list.append(oda)

        context = super(ODAsSectionView, self).get_context_data(**kwargs)
        initial = [{'oda_field': x.oda_field, 'active_icon_field': x.active_icon_field,
                    'completed_icon_field': x.completed_icon_field} for x in
                   self.object.odas_field.all().filter(section_field=section)]

        if self.request.POST:
            context.update({
                'formset': self.get_image_formset_class()(self.request.POST, self.request.FILES, initial=initial
                                                          ),
                'background_image': background_image
            })
        else:

            context.update({
                'formset': self.get_image_formset_class()(initial=initial),
                'background_image': background_image,
                'odas_list': odas_list,
                'odas_to_avoid_list': odas_to_avoid_list
            })
        return context

    def form_valid(self, form):
        section = self.kwargs['section']
        context = self.get_context_data()
        formset = context['formset']
        current_odas_list = []
        if formset.is_valid():
            if formset.has_changed():
                for form in formset:
                    a = form.save_form(self.request.user.profile, section)
                    current_odas_list.append(a.pk)
                    if a not in self.object.odas_field.all().filter(section_field=section):
                        self.object.odas_field.add(a)
                self.object.save()
                self.object.update_odas(section, current_odas_list)
            return HttpResponseRedirect(self.get_success_url())
        else:
            i = 1
            for form in formset:
                if form['oda_name'].errors:
                    sweetify.error(self.request,
                                   "Error en el nombre de la ODA {}: {}".format(i, form.errors['oda_name'][0]),
                                   persistent='Ok')
                    break

                if form['active_icon_field'].errors:
                    sweetify.error(self.request,
                                   "Error en el ícono 1 de la ODA {}: {}".format(i,
                                                                                 form.errors['active_icon_field'][0]),
                                   persistent='Ok')
                    break

                if form['completed_icon_field'].errors:
                    sweetify.error(
                        self.request,
                        "Error en el ícono 2 de la ODA {}: {}".format(i,
                                                                      form.errors['completed_icon_field'][0]),
                        persistent='Ok')
                    break
                i += 1
            return render(self.request, self.template_name, context=context)


class ODAsPositionView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    form_class = ODAsPositionForm
    template_name = 'studio/dashboard/materias-edit-position.html'

    def get_context_data(self, **kwargs):
        section = self.kwargs['section']
        pk = self.kwargs['pk']
        context = super(ODAsPositionView, self).get_context_data(**kwargs)
        context.update({'pk': pk, 'section': section})
        return context

    def get(self, request, *args, **kwargs):
        section = self.kwargs['section']
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])

        if section <= 0:
            return redirect(to='materias_sections_view', pk=self.kwargs['pk'])
        context = self.get_context_data()
        if section <= subject.number_of_sections:
            section_img = subject.sections_images[section-1]
            form = ODAsPositionForm(initial={'name_field': subject.name})
            odas_list = subject.odas.filter(section_field=section)
            context.update({'form': form, 'section_img': section_img, 'odas_list': odas_list})
            return render(request, self.template_name, context=context)
        else:
            return redirect(to='odas_preview_view', pk=subject.pk)

    def form_valid(self, form):
        section = self.kwargs['section']
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])
        odas_to_save = subject.odas.filter(section_field=section)
        i = 1
        for oda in odas_to_save:
            zone = self.request.POST.get('p-block-{}'.format(i))
            oda.zone = zone.split('-')[1]
            oda.save()
            i += 1

        section += 1
        return redirect(to='odas_position_view', pk=subject.pk, section=section)


class ODAsPreviewView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/materias-edit-preview.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])
        section_images_list = subject.sections_images
        odas_list = []
        section_counter = 1
        for section in subject.sections_images:
            odas_list.append(subject.odas.filter(section_field=section_counter))
            section_counter += 1

        content_images = zip(odas_list, section_images_list)
        return render(request, self.template_name, {'content_images': content_images, 'pk': pk})

    def post(self, request, *args, **kwargs):
        subject = SubjectModel.objects.get(pk=self.kwargs['pk'])
        for tag in subject.tags:
            tag.temporal = False
            tag.save()

        for image in subject.sections_images:
            image.temporal = False
            image.save()

        for oda_in_subject in subject.odas:
            oda_in_subject.temporal = False
            oda_in_subject.active_icon_field.temporal = False
            oda_in_subject.active_icon_field.save()
            oda_in_subject.completed_icon_field.temporal = False
            oda_in_subject.completed_icon_field.save()
            oda_in_subject.save()

        return redirect(to="materias_view")


class ODADashboardView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    model = ODAModel
    template_name = 'studio/dashboard/odas.html'
    context_object_name = 'odas_list'

    def get_context_data(self, **kwargs):
        context = super(ODADashboardView, self).get_context_data(**kwargs)
        tags_list = []
        tags = TagModel.objects.all()
        for tag in tags:
            if len(tag.odas) > 0:
                tags_list.append(tag)

        subjects_list = SubjectModel.objects.all()
        context.update({'subject_list': subjects_list, 'tags_list': tags_list})
        return context


class ODACreateView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/pages/odasTest.html'
    form_class = ODAUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ODACreateView, self).get_context_data(**kwargs)
        subjects_list = SubjectModel.objects.all()
        tags_list = TagModel.objects.all()

        context.update({'subject_list': subjects_list, 'tags_list': tags_list})
        return context

    def form_valid(self, form):
        pass


class ODAUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/pages/odasTest.html'
    form_class = ODAUpdateForm

    def get_object(self, queryset=None):
        return ODAModel.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ODAUpdateView, self).get_context_data(**kwargs)
        subjects_list = self.object.subject
        tags_list = self.object.tags

        context.update({'subject_list': subjects_list, 'tags_list': tags_list})
        return context

    def form_valid(self, form):
        form.save_form()


class ODAsRedirect(View):
    def dispatch(self, request, *args, **kwargs):
        view = kwargs.get('view')
        section = kwargs.get('section')
        pk = kwargs.get('pk')
        if view == 'odas_preview_view':
            return redirect(to='odas_position_view', pk=pk,
                            section=SubjectModel.objects.get(pk=pk).number_of_sections_field)

        if section == 1:
            if view == 'odas_section_view':
                return redirect(to='materias_sections_view', pk=pk)
            if view == 'odas_position_view':
                return redirect(to='odas_section_view', pk=pk,
                                section=SubjectModel.objects.get(pk=pk).number_of_sections_field)
        else:
            return redirect(view, pk=pk, section=(kwargs.get('section')-1))
