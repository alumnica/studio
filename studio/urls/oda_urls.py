from django.urls import path

from studio.views.oda_views import *

urlpatterns = [
    path(('odas_section/<section>, <subject_name>'), ODAsSectionView.as_view(), name='odas_section_view'),
]