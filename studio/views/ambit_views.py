from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView, UpdateView
from sweetify import sweetify
from studio.forms.ambit_forms import *


class CreateAmbitView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = CreateAmbitForm

    def get(self, request, *args, **kwargs):
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all().filter(temporal_field=False)
        return render(request, self.template_name, {'form': self.form_class, 'subjects': subjects, 'tags': tags})

    def form_valid(self, form):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito').split(',')
        color = self.request.POST.get('color')
        form.save_form(self.request.user, subjects, tags, color)
        return redirect(to='ambits_view')

    def form_invalid(self, form):
        if form['name_field'].errors:
            sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        if form['position_field'].errors:
            sweetify.error(self.request, form.errors['position_field'][0], persistent='Ok')
        if form['ap'].errors:
            sweetify.error(self.request, form.errors['ap'][0], persistent='Ok')
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all()
        return render(self.request, self.template_name, {'form': form, 'subjects': subjects, 'tags': tags})

class UpdateAmbitView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = UpdateAmbitForm

    def get_object(self, queryset=None):
        return AmbitModel.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UpdateAmbitView, self).get_context_data(**kwargs)
        ambits = AmbitModel.objects.all().exclude(pk=self.kwargs['pk'])
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all().filter(temporal_field=False)
        context.update({'subjects': subjects, 'tags': tags, 'ambits': ambits})
        return context

    def form_valid(self, form):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito').split(',')
        color = self.request.POST.get('color')
        form.save_form(subjects, tags, color)
        return redirect(to='ambits_view')


class AmbitView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos.html'
    queryset = AmbitModel.objects.all()
    context_object_name = 'ambit_list'
