from django.urls import path

from django_h5p.views import UploadH5PackageView, PackageView

urlpatterns = [
    path('', UploadH5PackageView.as_view(), name='upload_h5p_view'),
    path('package/<int:pk>/', PackageView.as_view(), name='package_view'),
    path('package/<str:job_id>/', PackageView.as_view(), name='package_view'),
]