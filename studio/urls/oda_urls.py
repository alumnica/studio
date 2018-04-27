from django.urls import path

from studio.views.oda_views import *

urlpatterns = [
    path('odas_section/<int:pk>,<int:section>/', ODAsSectionView.as_view(), name='odas_section_view'),
    path('odas_position/<int:pk>,<int:section>/', ODAsPositionView.as_view(), name='odas_position_view'),
    path('odas_preview/<int:pk>/', ODAsPreviewView.as_view(), name='odas_preview_view'),
    path('odas_back/<slug:view>, <int:pk>, <int:section>/', ODAsRedirect.as_view(), name='go_back_view'),
    path('odas_dashboard/', ODADashboardView.as_view(), name='oda_dashboard_view'),
    path('odas_update/<int:pk>', ODAUpdateView.as_view(), name='odas_update_view'),
    path('odas_create/', ODACreateView.as_view(), name='odas_create_view'),
]
