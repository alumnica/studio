from django.urls import path

from studio.views.oda_views import *

urlpatterns = [
    path('odas_section/<int:pk>,<int:section>/', ODAsSectionView.as_view(), name='odas_section_view'),
]