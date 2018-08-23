"""studio_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from django_h5p.api_viewsets import H5PackageViewSet, H5PLibraryViewSet, H5PackageDependencyViewSet, \
    PreloadedCSSViewSet, PreloadedJSViewSet, EmbedTypeViewSet, PackageUploadAPIView, JobAPIView
from studio import api_viewsets
from studio.views.user_views import IndexView
from django.views.i18n import JavaScriptCatalog

router = routers.DefaultRouter()
router.register(r'images', api_viewsets.ImageViewSet)
router.register(r'evaluations', api_viewsets.EvaluationViewSet)
router.register(r'h5packages', H5PackageViewSet)
router.register(r'h5p_libraries', H5PLibraryViewSet)
router.register(r'h5package_dependencies', H5PackageDependencyViewSet)
router.register(r'preloaded_css', PreloadedCSSViewSet)
router.register(r'preloaded_js', PreloadedJSViewSet)
router.register(r'embed_types', EmbedTypeViewSet)


urlpatterns = [
                  path('', IndexView.as_view(), name="index_view"),
                  path('users/', include('studio.urls.user_urls')),
                  path('supervisor/', include('studio.urls.supervisor_urls')),
                  path('ambitos/', include('studio.urls.ambit_urls')),
                  path('subjects/', include('studio.urls.subject_urls')),
                  path('odas/', include('studio.urls.oda_urls')),
                  path('images/', include('studio.urls.image_urls')),
                  path('momentos/', include('studio.urls.moment_urls')),
                  path('h5p/', include('django_h5p.urls')),
                  path('admin/', admin.site.urls),
                  path('api/', include(router.urls)),
                  path('api/zip_files/', PackageUploadAPIView.as_view(), name='package_upload_view'),
                  path('api/jobs/<str:job_id>/', JobAPIView.as_view(), name='job_detail_view'),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('registration', include('django.contrib.auth.urls')),
                  path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
