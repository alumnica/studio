from django.urls import path

from studio.views.oda_views import *

urlpatterns = [
    path('position/<int:pk>,<int:section>/', ODAsPositionView.as_view(), name='odas_position_view'),
    path('back/<slug:view>, <int:pk>, <int:section>/', ODAsRedirect.as_view(), name='go_back_view'),
    path('dashboard/', ODADashboardView.as_view(), name='oda_dashboard_view'),
    path('update/<int:pk>', ODAUpdateView.as_view(), name='odas_update_view'),
    path('create/', ODACreateView.as_view(), name='odas_create_view'),
    path('delete_oda/<int:pk>/', DeleteODAView.as_view(), name='delete_oda_view'),
]
