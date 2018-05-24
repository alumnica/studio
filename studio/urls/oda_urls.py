from django.urls import path

from studio.views.oda_views import ODAsPositionView, ODAsPreviewView, ODAsRedirect, ODADashboardView, \
    ODAUpdateView, ODACreateView, ODAsSectionView

urlpatterns = [
    path('position/<int:pk>,<int:section>/', ODAsPositionView.as_view(), name='odas_position_view'),
    path('preview/<int:pk>/', ODAsPreviewView.as_view(), name='odas_preview_view'),
    path('back/<slug:view>, <int:pk>, <int:section>/', ODAsRedirect.as_view(), name='go_back_view'),
    path('dashboard/', ODADashboardView.as_view(), name='oda_dashboard_view'),
    path('update/<int:pk>', ODAUpdateView.as_view(), name='odas_update_view'),
    path('create/', ODACreateView.as_view(), name='odas_create_view'),
]
