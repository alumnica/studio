from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from alumnica_model.models import Moment


class MomentsView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
