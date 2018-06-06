from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from alumnica_model.models import Ambit, users


class AproveToPublishDashboard(LoginRequiredMixin, ListView):
    login_url = "login_view"
    template_name = ""
    queryset = Ambit.objects.filter(is_draft=False, is_published=False)
    context_object_name = "ambits_2_aprove_list"

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AproveToPublishDashboard, self).dispatch(self, request, *args, **kwargs)


class AmbitPreviewView(LoginRequiredMixin, DetailView):
    login_url = "login_view"
    template_name = ""

    def dispatch(self, request, *args, **kwargs):
        if request.user.type != users.TYPE_SUPERVISOR:
            return redirect(to="dashboard_view")
        else:
            return super(AmbitPreviewView, self).dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AmbitPreviewView, self).get_context_data(**kwargs)
        ambit = Ambit.objects.get(pk=kwargs['pk'])
        context.update({'ambit': ambit})
        return context