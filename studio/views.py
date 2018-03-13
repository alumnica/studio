from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import FormView, RedirectView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.base import View
from studio.forms import UserForm, AdministratorForm, LearnerForm


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = '/users/profile/'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfile(LoginRequiredMixin, DetailView):
    template_name = "profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserSignUp(View):
    user_form_class = UserForm
    profile_form_class = LearnerForm
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/users/profile')
        # Here I make instances of my form classes and pass them None
        # which tells them that there is no additional data to display (errors, for example)
        user_form = self.user_form_class(None)
        profile_form = self.profile_form_class(None)
        print("holi")
        # and then just pass them to my template
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})





