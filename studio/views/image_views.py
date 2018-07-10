from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin


class ImageLibraryView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, TemplateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/biblioteca.html'
