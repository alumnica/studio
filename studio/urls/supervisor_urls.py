from django.urls import path

from studio.views.supervisor_views import ApproveToPublishDashboard, AmbitPreviewView, ODAsPositionSubjectPreview, \
    MicroodaPreview

urlpatterns = [
    path('', ApproveToPublishDashboard.as_view(), name='approve_dashboard_view'),
    path('ambit_preview/<int:pk>/', AmbitPreviewView.as_view(), name='ambit_preview_view'),
    path('subject_preview/<int:pk>/', ODAsPositionSubjectPreview.as_view(), name='subject_preview_view'),
    path('oda_preview/<int:pk>/', MicroodaPreview.as_view(), name='oda_preview_view'),
    ]