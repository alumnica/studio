from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ImageLibraryView(LoginRequiredMixin, TemplateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/biblioteca.html'
