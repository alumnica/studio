from django.urls import path

from studio.views.oda_views import *

urlpatterns = [
    path('odas_section/<int:pk>,<int:section>/', ODAsSectionView.as_view(), name='odas_section_view'),
    path('odas_position/<int:pk>,<int:section>/', ODAsPositionView.as_view(), name='odas_position_view'),
    path('odas_preview/<int:pk>/', ODAsPreviewView.as_view(), name='odas_preview_view'),
]