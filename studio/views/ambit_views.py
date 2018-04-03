from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from studio.forms.ambit_forms import CreateAmbitForm


class CreateAmbitView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/pages/test.html'
    form_class = CreateAmbitForm

    def form_valid(self, form):
        form.save_form(self.request.user)
        return redirect(to='thanks')


class AmbitView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'