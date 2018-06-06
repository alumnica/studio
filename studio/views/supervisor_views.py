from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from alumnica_model.models import Ambit


class AproveToPublishDashboard(LoginRequiredMixin, ListView):
    login_url = "login_view"
    template_name = ""
    queryset = Ambit.objects.filter(is_draft=False, is_published=False)
    context_object_name = "ambits_2_aprove_list"