from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from alumnica_model.models import Moment


class MomentsView(LoginRequiredMixin, ListView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    queryset = Moment.objects.all()
    context_object_name = 'moments_list'