from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from studio.forms.subject_forms import CreateSubjectForm


class CreateSubjectView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/pages/test.html'
    form_class = CreateSubjectForm

    def form_valid(self, form):
        return redirect(to='thanks')