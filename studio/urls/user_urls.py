from django.urls import path

from studio.views.user_views import LogoutView, LoginView, ProfileView, CreateUserView, UpdateUserView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('dashboard/', ProfileView.as_view(), name='dashboard_view'),
    path('test/', CreateUserView.as_view(), name='test_create_user_view'),
    path('test_update/<int:pk>/', UpdateUserView.as_view(), name='test_update_user_view'),
]
