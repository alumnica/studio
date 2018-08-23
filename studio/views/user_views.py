from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, CreateView, ListView
from django.views.generic.base import TemplateView, RedirectView
from sweetify import sweetify

from alumnica_model.mixins import OnlyContentCreatorAndSupervisorMixin, OnlySupervisorMixin
from alumnica_model.models import Ambit, Subject, Moment, ODA, AuthUser
from alumnica_model.models.users import TYPE_SUPERVISOR, TYPE_CONTENT_CREATOR
from studio.forms.user_forms import UserLoginForm, CreateUserForm, UpdateUserForm


class LoginView(FormView):
    """
    Login user view
    """
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
    """
    Logout user view
    """
    pattern_name = 'login_view'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, OnlyContentCreatorAndSupervisorMixin, FormView):
    """
    Profile user view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        ambits = Ambit.objects.all().count()
        ambitsToPublish = Ambit.objects.filter(is_draft=False, is_published=False)
        subjects = Subject.objects.all().count()
        moments = Moment.objects.all().count()
        odas = ODA.objects.all().count()
        return render(request, self.template_name,
                      {'form': self.form_class, 'ambits': ambits, 'subjects': subjects, 'odas': odas,
                       'moments': moments, 'ambitsToPublish': ambitsToPublish})


class UsersView(LoginRequiredMixin, OnlySupervisorMixin, ListView):
    """
    Users dashboard view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users.html'
    queryset = AuthUser.objects.filter(Q(user_type=TYPE_SUPERVISOR) | Q(user_type=TYPE_CONTENT_CREATOR))
    context_object_name = 'users_list'


class CreateUserView(LoginRequiredMixin, OnlySupervisorMixin, CreateView):
    """
    Create new AuthUser object view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users-edit.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('dashboard_view')

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        user = form.save()
        sweetify.success(self.request, "Usuario creado", persistent='Ok')
        return super(CreateUserView, self).form_valid(form)


class UpdateUserView(LoginRequiredMixin, OnlySupervisorMixin, UpdateView):
    """
    Update existing user view
    """
    login_url = 'login_view'
    template_name = 'studio/dashboard/users-edit.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('dashboard_view')

    def get_object(self, queryset=None):
        return AuthUser.objects.get(pk=self.kwargs['pk'])

    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        user = form.save()
        sweetify.success(self.request, "Información de usuario actualizada", persistent='Ok')
        return super(UpdateUserView, self).form_valid(form)
