from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView
from sweetify import sweetify

from alumnica_model.models import AmbitModel, SubjectModel, TagModel
from studio.forms.ambit_forms import CreateAmbitForm


class CreateAmbitView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos-edit.html'
    form_class = CreateAmbitForm

    def get(self, request, *args, **kwargs):
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'subjects': subjects, 'tags': tags})

    def form_valid(self, form):
        subjects = self.request.POST.get('class_name')
        tags = self.request.POST.get('tags-ambito').split(',')
        color = self.request.POST.get('color')
        image = self.request.FILES['image_file']
        form.save_form(self.request.user, subjects, tags, color, image)
        return redirect(to='ambitos_view')

    def form_invalid(self, form):
        if form['name_field'].errors:
            sweetify.error(self.request, form.errors['name_field'][0], persistent='Ok')
        if form['position_field'].errors:
            sweetify.error(self.request, form.errors['position_field'][0], persistent='Ok')
        subjects = SubjectModel.objects.all()
        tags = TagModel.objects.all()
        return render(self.request, self.template_name, {'form': self.form_class, 'subjects': subjects, 'tags': tags})




class AmbitView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/ambitos.html'
    queryset = AmbitModel.objects.all()
    context_object_name = 'ambit_list'