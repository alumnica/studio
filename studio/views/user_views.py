from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView, RedirectView
from sweetify import sweetify
from django.utils.translation import gettext_lazy as _
from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin, OnlySupervisorMixin
from alumnica_model.models import Ambit, Subject, Moment, ODA
from studio.forms.user_forms import UserLoginForm, CreateUserForm


class IndexView(TemplateView):
    login_url = 'login_view'
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


class ProfileView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        ambits = Ambit.objects.all().count()
        ambitsToPublish = Ambit.objects.filter(is_draft=False, is_published=False)
        subjects = Subject.objects.all().count()
        moments = Moment.objects.all().count()
        odas = ODA.objects.all().count()
        return render(request, self.template_name, {'form': self.form_class, 'ambits': ambits, 'subjects': subjects, 'odas':odas, 'moments': moments, 'ambitsToPublish': ambitsToPublish})


class CreateUserView(LoginRequiredMixin, OnlySupervisorMixin, FormView):
    login_url = 'login_view'
    template_name = 'studio/pages/test.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('dashboard_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        user = form.save()
        sweetify.success(self.request, _('User created'), persistent='Ok')
        return super(CreateUserView, self).form_valid(form)