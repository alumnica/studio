from django.urls import path, re_path
from . import views


urlpatterns = [
    path('signup/',views.UserSignUp.as_view(), name='signup'),
    path('profile/',views.UserProfile.as_view(), name='profile'),
    path('logout/',views.LogoutView.as_view(), name='logout'),
    path('login/',views.LoginView.as_view(), name='login'),
]