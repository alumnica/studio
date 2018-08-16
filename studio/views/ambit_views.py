from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, FormView, UpdateView
from sweetify import sweetify

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin
from alumnica_model.models import users
from studio.forms.ambit_forms import *


class CreateAmbitView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = CreateAmbitForm

    def get(self, request, *args, **kwargs):
        """
Gets data needed to create Ambitos
        :return: Arguments containing form, temporal Subjects list, tags list, ambitos list and ambitos space flag
        """
        ambits = Ambit.objects.all()
        subjects = Subject.objects.filter(temporal=False).filter(ambit=None)
        tags = Tag.objects.all()
        ambit_space = Ambit.objects.all().filter(is_published=True).count() < 30
        return render(request, self.template_name, {'form': self.form_class, 'subjects': subjects,
                                                    'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})

    def post(self, request, *args, **kwargs):
        """
Retrieves data from template to create new Ambito
        """
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
            ambit, published = form.save_form(request.user, subjects, tags, color)
            if not published:
                sweetify.error(
                    self.request,
                    _('Error saving ámbito {}. Not all subjects are finalized'.format(ambit.name)), persistent='Ok')
                return redirect('update_ambit_view', pk=ambit.pk)
        return redirect(to='ambits_view')


class UpdateAmbitView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = UpdateAmbitForm

    def dispatch(self, request, *args, **kwargs):
        """
Redirects if Ambito to update is published and current user is not allowed to edit it
        """
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        if ambit.is_published:
            if self.request.user.user_type == users.TYPE_CONTENT_CREATOR:
                sweetify.error(self.request,
                               _('It is not possible to edit Ámbito {} because is already published'.format(
                                   ambit.name)),
                               persistent='Ok')
                return redirect(to='ambits_view')
        return super(UpdateAmbitView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
Gets Ambito object from pk in arguments
        """
        return Ambit.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Gets all available objects to edit Ambito properties
        :return: Context containing Subjects without ambito list, tags list, ambitos list and ambitos space flag
        """
        context = super(UpdateAmbitView, self).get_context_data(**kwargs)
        ambits = Ambit.objects.all().exclude(pk=self.kwargs['pk'])
        subjects = Subject.objects.all().exclude(ambit=self.object).filter(ambit=None)
        tags = Tag.objects.all().filter()
        ambit_space = Ambit.objects.all().filter(is_published=True).count() < 30
        context.update({'subjects': subjects, 'tags': tags, 'ambits': ambits, 'ambit_space': ambit_space})
        return context

    def post(self, request, *args, **kwargs):
        """
Retrieves properties for an existing Ambito
        """
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
            ambit, published = form.save_form(subjects, tags, color)
            if not published:
                sweetify.error(
                    self.request,
                    _('Error saving ámbito {}. Not all subjects are finalized'.format(ambit.name)), persistent='Ok')

                return redirect('update_ambit_view', pk=ambit.pk)
        return redirect(to='ambits_view')


class AmbitView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos.html'
    queryset = Ambit.objects.all()
    context_object_name = 'ambit_list'


class DeleteAmbitView(View):
    def dispatch(self, request, *args, **kwargs):
        """
Deletes Ambito from database
        """
        Ambit.objects.get(pk=self.kwargs['pk']).pre_delete()
        return redirect('ambits_view')


class UnPublishAmbitView(View):
    def dispatch(self, request, *args, **kwargs):
        """
Changes Ambito to unpublished and draft object:
        """
        ambit = Ambit.objects.get(pk=self.kwargs['pk'])
        ambit.is_published = False
        ambit.is_draft = True
        ambit.save()
        return redirect('ambits_view')
