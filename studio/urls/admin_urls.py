from django.urls import path

from studio.views.admin_views import  SyncDB, CreateUserView, UpdateUserView, UsersView

urlpatterns = [    
	path('sync/', SyncDB.as_view(), name='sync_firestore_view'),
    path('users/', UsersView.as_view(), name='users_view'),
    path('create_user/', CreateUserView.as_view(), name='create_user_view'),
    path('user_update/<int:pk>/', UpdateUserView.as_view(), name='update_user_view'),
]
