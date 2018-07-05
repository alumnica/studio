from django.urls import path

from studio.views.supervisor_views import ApproveToPublishDashboard

urlpatterns = [
    path('', ApproveToPublishDashboard.as_view(), name='approve_dashboard_view'),
]