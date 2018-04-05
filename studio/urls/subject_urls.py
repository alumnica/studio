from django.urls import path
from studio.views.subject_views import *


urlpatterns = [
    path('create_subject/', CreateSubjectView.as_view(), name='create_subject_view'),
    path('subjects/', SubjectView.as_view(), name='materias_view'),
]