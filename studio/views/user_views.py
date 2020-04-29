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
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from django.conf import settings


# Initialize the default app
cred = credentials.Certificate(settings.BASE_DIR + '/alumnica-app-firebase-adminsdk-w2lxi-0d9945b073.json')

default_app = firebase_admin.initialize_app(cred)

print(default_app.name)  # "[DEFAULT]"




class LoginView(FormView):
    """
    Login user view
    """
    form_class = UserLoginForm
    template_name = 'studio/pages/login.html'

    def is_authenticated(self, user):
        print ('in auth --> ' + str (user))



    def dispatch(self, request, *args, **kwargs):
        print ('login view')
        print (request)
        print (args)
        print (kwargs)
        print (request.user)
        #if request.user.is_authenticated:
        if self.is_authenticated(request.user):
            if not request.user.is_staff:
                return redirect(to='dashboard_view')
            else:
                return redirect(to='/admin/')
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print ('form valid')
        print (form)
        login(self.request, form.get_user())
        return redirect(to='dashboard_view')

    def form_invalid(self, form):
        print ('form invalid')
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

    def create_user_firebase (self, email, password, role):
        print ('in create user')
        user = auth.create_user(
            email=email,
            email_verified=False,
            #phone_number='+15555550100',
            password=password,
            #display_name='John Doe',
            #photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)

        auth.set_custom_user_claims(user.uid, {role: True})
        print('Sucessfully created new user: {0}'.format(user.uid))


    def form_invalid(self, form):
        sweetify.error(self.request, form.errors['email'][0], persistent='Ok')
        print ('in from invalid ' )
        print (self)
        print (form)
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        print(form)
        print ('in from valid ' )
        print (self)
        user = form.instance
        print (user)
        print (user.password)
        print (user.email)
        
        self.create_user_firebase (user.email, user.password, user.user_type)
        sweetify.success(self.request, "Usuario creado", persistent='Ok')
        context = self.get_context_data()
        print (context)
        print (self.success_url)
        return redirect (self.success_url)
        #return self.render_to_response(context)

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
