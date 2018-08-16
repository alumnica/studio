from django.urls import path

from studio.views.moment_views import MomentsView, CreateMomentView, UpdateMomentView, DeleteMomentView

urlpatterns = [
    path('', MomentsView.as_view(), name='momentos_view'),
    path('create/', CreateMomentView.as_view(), name='create_momentos_view'),
    path('update/<int:pk>/', UpdateMomentView.as_view(), name='update_momentos_view'),
    path('delete/<int:pk>/', DeleteMomentView.as_view(), name='delete_momentos_view'),
]
