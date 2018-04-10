from django.urls import path
from studio.views.subject_views import *


urlpatterns = [
    path(('create_subject/'), CreateSubjectView.as_view(), name='create_subject_view'),
    path(('subject_sections/<subject_name>'), SubjectSectionsView.as_view(), name='materias_sections_view'),
    path(('odas_section/<section>, <subject_name>'), ODAsSectionView.as_view(), name='odas_section_view'),
    path('subjects/', SubjectView.as_view(), name='materias_view'),
]