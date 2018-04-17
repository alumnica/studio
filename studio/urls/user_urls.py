from django.urls import path
from studio.views.user_views import *

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('dashboard/', ProfileView.as_view(), name='dashboard_view'),
]
