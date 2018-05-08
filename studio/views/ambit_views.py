import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from rest_framework.reverse import reverse_lazy
from sweetify import sweetify
from studio.forms.ambit_forms import *
from studio.serializers import ImageHyperlinkedModelSerializer


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
        if action == 'draft':
            form.save_as_draft(request.user, subjects, tags, color)
        elif action == 'publish':
            form.save_form(request.user, subjects, tags, color)
        return redirect(to='ambits_view')


class UpdateAmbitView(LoginRequiredMixin, UpdateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = UpdateAmbitForm

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

        if action == 'draft':
            form.save_as_draft(subjects, tags, color)
        elif action == 'publish':
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
        return redirect('materias_view')


def ImagesTestView(request):
    if request.method == "GET":
        r = requests.get('http://localhost:8000/api/images/')
        json = r.json()
        return render(request, 'studio/pages/test.html', {'json': json})

    return render(request, 'studio/pages/test.html')