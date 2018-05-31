from django.urls import path

from studio.views.subject_views import CreateSubjectView, UpdateSubjectView, SubjectView, DeleteSubjectView

urlpatterns = [
    path('', SubjectView.as_view(), name='materias_view'),
    path('create_subject/', CreateSubjectView.as_view(), name='create_subject_view'),
    path('update_subject/<int:pk>/', UpdateSubjectView.as_view(), name='update_subject_view'),
    path('delete_subject/<int:pk>/', DeleteSubjectView.as_view(), name='delete_subject_view'),
]
