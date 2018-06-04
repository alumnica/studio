from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView

from alumnica_model.models import Moment, Tag
from studio.forms.moment_forms import MomentCreateForm


class MomentsView(LoginRequiredMixin, CreateView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/momentos.html'
    form_class = MomentCreateForm

    def get_context_data(self, **kwargs):
        moments_list = Moment.objects.all()
        tags = Tag.objects.all()
        context = super(MomentsView, self).get_context_data(**kwargs)
        context.update({'moments_list': moments_list, 'tags':tags})
        return context

    def form_invalid(self, form):
        pass

    def form_valid(self, form):
        form.save_form(self.request.user)
        return redirect(to='momentos_view')