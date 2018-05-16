import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from sweetify import sweetify

from alumnica_model.alumnica_entities.users import UserType
from studio.forms.ambit_forms import *


class CreateAmbitView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = CreateAmbitForm

    def get(self, request, *args, **kwargs):
        ambits = AmbitModel.objects.all()
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all().filter()
        ambit_space = AmbitModel.objects.all().filter(is_published_field=True).count() < 30
        return render(request, self.template_name, {'form': self.form_class, 'subjects': subjects,
                                                    'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})

    def post(self, request, *args, **kwargs):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito')
        if tags is not None:
            tags = tags.split(',')
        color = self.request.POST.get('color')
        action = self.request.POST.get('action')
        form = CreateAmbitForm(self.request.POST, self.request.FILES)
        form.is_valid()
        if action == 'save':
            form.save_as_draft(request.user, subjects, tags, color)
        elif action == 'eva-publish':
            form.save_form(request.user, subjects, tags, color)
        return redirect(to='ambits_view')


class UpdateAmbitView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = UpdateAmbitForm

    def dispatch(self, request, *args, **kwargs):
        ambit = AmbitModel.objects.get(pk=self.kwargs['pk'])
        if ambit.is_published_field:
            if self.request.user.user_type == UserType.CONTENT_CREATOR:
                sweetify.error(self.request,
                               'No puedes editar el ámbito {} porque ya esta publicado'.format(ambit.name_field),
                               persistent='Ok')
                return redirect(to='ambits_view')
        return super(UpdateAmbitView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return AmbitModel.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UpdateAmbitView, self).get_context_data(**kwargs)
        ambits = AmbitModel.objects.all().exclude(pk=self.kwargs['pk'])
        subjects = SubjectModel.objects.all().exclude(ambit_field=self.object)
        tags = TagModel.objects.all().filter()
        ambit_space = AmbitModel.objects.all().filter(is_published_field=True).count() < 30
        context.update({'subjects': subjects, 'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})
        return context

    def post(self, request, *args, **kwargs):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito')
        if tags is not None:
            tags = tags.split(',')
        color = self.request.POST.get('color')
        action = self.request.POST.get('action')
        form = UpdateAmbitForm(self.request.POST, self.request.FILES)
        form.is_valid()

        if action == 'save':
            form.save_as_draft(subjects, tags, color)
        elif action == 'eva-publish':
            form.save_form(subjects, tags, color)
        return redirect(to='ambits_view')


class AmbitView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos.html'
    queryset = AmbitModel.objects.all()
    context_object_name = 'ambit_list'


class DeleteAmbitView(View):
    def dispatch(self, request, *args, **kwargs):
        AmbitModel.objects.filter(pk=self.kwargs['pk']).delete()
        return redirect('ambits_view')


class UnPublishAmbitView(View):
    def dispatch(self, request, *args, **kwargs):
        ambit = AmbitModel.objects.get(pk=self.kwargs['pk'])
        ambit.is_published_field = False
        ambit.is_draft = True
        ambit.save()
        return redirect('ambits_view')

