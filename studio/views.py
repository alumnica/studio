
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import FormView, RedirectView, DetailView
from django.contrib.auth import login, logout
from django.views.generic.base import View

from alumnica_model.alumnica_entities.users import UserType
from alumnica_model.models import AuthUser
from studio.forms import UserForm, AdministratorForm, LearnerForm, ContentCreatorForm, DataAnalystForm, UserLoginForm


class LoginView(View):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = '/users/profile/'
    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/users/profile')
        else:
            form=UserLoginForm(None)
            return render(request,"login.html",{'form':form})

    def post(self,request):
        form=UserLoginForm(data=request.POST)
        if form.is_valid:
            username=request.POST['username']
            password=request.POST['password']
            try:
                user=AuthUser.objects.get(username=username)
                print(username)
                print(password)

                if user.check_password(password):
                    login(request,user)
                    return redirect('/users/profile')
                else:
                    print('password didnt match')
                    form = UserLoginForm(None)
                    return render(request, "login.html", {'form': form})
            except AuthUser.DoesNotExist:
                form = UserLoginForm(None)
                return render(request, "login.html", {'form': form})

        else:
            print('form not valid')
            form = UserLoginForm(None)
            return render(request, "login.html", {'form': form})




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
    #forms
    user_form_class = UserForm
    learner_form_class = LearnerForm
    admin_form_class = AdministratorForm
    contentCreator_form_class = ContentCreatorForm
    dataAnalyst_form_class = DataAnalystForm

    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/users/profile')
        # Here I make instances of my form classes and pass them None
        # which tells them that there is no additional data to display (errors, for example)
        user_form = self.user_form_class(None)
        admin_form = self.admin_form_class(None)
        learner_form = self.learner_form_class(None)
        contentCreator_form = self.contentCreator_form_class(None)
        dataAnalyst_form = self.dataAnalyst_form_class(None)
        # and then just pass them to my template
        return render(request, self.template_name, {'user_form': user_form, 'admin_form': admin_form, 'learner_form': learner_form,
                                                    'contentCreator_form': contentCreator_form, 'dataAnalyst_form': dataAnalyst_form})

    def post(self, request, *args, **kwargs):
        userType=request.POST['user_type']
        password=request.POST['password1']
        user_form=UserForm(data=request.POST)
        user = user_form.save(commit=False)
        if user_form.is_valid:
            user.set_password(password)
            user.save()
            if userType == UserType.LEARNER:
                profile=user.profile
                print(profile)
                profile.experience_points_field=request.POST['experience_points_field']
                profile.save()
            return redirect('/users/login')

        return redirect(request, *args, **kwargs)





