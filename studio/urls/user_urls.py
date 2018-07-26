from django.urls import path

from studio.views.user_views import LogoutView, LoginView, ProfileView, CreateUserView, UpdateUserView, UsersView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('dashboard/', ProfileView.as_view(), name='dashboard_view'),
    path('', UsersView.as_view(), name='users_view'),
    path('create_user/', CreateUserView.as_view(), name='create_user_view'),
    path('user_update/<int:pk>/', UpdateUserView.as_view(), name='update_user_view'),
]
