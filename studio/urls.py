from django.urls import path

from . import views

urlpatterns = [
    path('signup_view/', views.UserSignUp.as_view(), name='signup_view'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login_view/', views.LoginView.as_view(), name='login_view'),
]
