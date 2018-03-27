from django.shortcuts import redirect
from django.views.generic import CreateView, FormView

from studio.forms.ambit_forms import CreateAmbitoForm


class CreateAmbitoView(FormView):
    template_name = ''
    form_class = CreateAmbitoForm

    def form_valid(self, form):
        color = self.request.POST.get('')
        form.save_form(self.request.user, color)
        return redirect(to = "")