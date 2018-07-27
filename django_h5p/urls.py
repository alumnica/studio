from django.urls import path

from django_h5p.api_viewsets import PackageUploadAPIView, JobAPIView
from django_h5p.views import UploadH5PackageView, PackageView, ThreeSixtyView

urlpatterns = [
    path('', UploadH5PackageView.as_view(), name='upload_h5p_view'),
    path('package/<int:pk>/', PackageView.as_view(), name='package_view'),
    path('package/<str:job_id>/', PackageView.as_view(), name='package_view'),
    path('360/', ThreeSixtyView.as_view()),
    path('api/zip_files/', PackageUploadAPIView.as_view()),
    path('api/jobs/<str:job_id>/', JobAPIView.as_view(), name='job_detail_view'),
]