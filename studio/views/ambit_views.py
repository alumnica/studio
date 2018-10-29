from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, FormView, UpdateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import users
from studio.forms.ambit_forms import *


class CreateAmbitView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, FormView):
    """
    Create new Ambito object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = CreateAmbitForm

    def get_context_data(self, **kwargs):
        ambits = Ambit.objects.all()
        subjects = Subject.objects.filter(temporal=False).filter(ambit=None)
        tags = Tag.objects.all()
        ambit_space = Ambit.objects.all().filter(is_published=True).count() < 30

        context = super(CreateAmbitView, self).get_context_data()
        context.update({'form': self.form_class, 'subjects': subjects,
                                                    'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})
        return context

    def form_valid(self, form):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito')
        if tags is not None and tags != '':
            tags = tags.split(',')
        color = self.request.POST.get('color')
        action = self.request.POST.get('action')

        if action == 'save':
            form.save_as_draft(self.request.user, subjects, tags, color)
        elif action == 'eva-publish':
            ambit, published = form.save_form(self.request.user, subjects, tags, color)
            if not published:
                sweetify.error(
                    self.request,
                    'Error al guardar el ámbito {}. No todas las materias asignadas están finalizadas'.format(
                        ambit.name), persistent='Ok')
                return redirect('update_ambit_view', pk=ambit.pk)
        return redirect(to='ambits_view')

    def form_invalid(self, form):
        error = ''
        if form['name'].errors:
            error = form.errors['name'][0]
        elif form['ap'].errors:
            error = form.errors['ap'][0]
        elif form['aU'].errors:
            error = form.errors['aU'][0]
        elif form['bU'].errors:
            error = form.errors['bU'][0]
        elif form['cU'].errors:
            error = form.errors['cU'][0]

        sweetify.error(self.request, error, persistent='Ok')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class UpdateAmbitView(LoginRequiredMixin, UpdateView):
    """
    Update existing Ambito view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = UpdateAmbitForm

    def dispatch(self, request, *args, **kwargs):
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        if ambit.is_published:
            if self.request.user.user_type == users.TYPE_CONTENT_CREATOR:
                sweetify.error(self.request,
                               'No puedes editar el ámbito {} porque ya está publicado'.format(
                                   ambit.name),
                               persistent='Ok')
                return redirect(to='ambits_view')
        return super(UpdateAmbitView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Ambit.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UpdateAmbitView, self).get_context_data(**kwargs)
        ambits = Ambit.objects.all().exclude(pk=self.kwargs['pk'])
        subjects = Subject.objects.all().exclude(ambit=self.object).filter(ambit=None)
        tags = Tag.objects.all().filter()
        ambit_space = Ambit.objects.all().filter(is_published=True).count() < 30
        context.update({'subjects': subjects, 'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})
        return context

    def form_valid(self, form):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito')
        if tags is not None and tags != '':
            tags = tags.split(',')
        color = self.request.POST.get('color')
        action = self.request.POST.get('action')

        if action == 'save':
            form.save_as_draft(subjects, tags, color, self.kwargs['pk'])
        elif action == 'eva-publish':
            ambit, published = form.save_form(subjects, tags, color, self.kwargs['pk'])
            if not published:
                sweetify.error(
                    self.request,
                    'Error al guardar el ámbito {}. No todas las materias asignadas están finalizadas'.format(
                        ambit.name), persistent='Ok')
                return redirect('update_ambit_view', pk=ambit.pk)
        return redirect(to='ambits_view')

    def form_invalid(self, form):
        error = ''
        if form['name'].errors:
            error = form.errors['name'][0]
        elif form['ap'].errors:
            error = form.errors['ap'][0]
        elif form['aU'].errors:
            error = form.errors['aU'][0]
        elif form['bU'].errors:
            error = form.errors['bU'][0]
        elif form['cU'].errors:
            error = form.errors['cU'][0]

        sweetify.error(self.request, error, persistent='Ok')
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class AmbitView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    """
    Ambit dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos.html'
    queryset = Ambit.objects.all()
    context_object_name = 'ambit_list'


class DeleteAmbitView(View):
    """
    Deletes Ambito object
    """

    def dispatch(self, request, *args, **kwargs):
        Ambit.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect('ambits_view')


class UnPublishAmbitView(View):
    """
    Unpublishes Ambito object, changing is_publish flag to false and is_draft flag to true
    """

    def dispatch(self, request, *args, **kwargs):
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        ambit.is_published = False
        ambit.is_draft = True
        ambit.save()
        return redirect('ambits_view')
