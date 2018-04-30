from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.views.generic.base import TemplateView, RedirectView
from sweetify import sweetify

from alumnica_model.models import AmbitModel, SubjectModel
from studio.forms.user_forms import UserLoginForm


class IndexView(TemplateView):
    template_name = 'studio/pages/index.html'


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'studio/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return redirect(to='dashboard_view')
            else:
                return redirect(to='/admin/')
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(to='dashboard_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['password'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)


class LogoutView(RedirectView):
    pattern_name = 'login_view'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        ambits = AmbitModel.objects.all().count()
        subjects = SubjectModel.objects.all().count()
        return render(request, self.template_name, {'form': self.form_class, 'ambits': ambits, 'subjects': subjects})