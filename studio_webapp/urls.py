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
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from studio import api_viewsets
from studio.views.user_views import IndexView
from django.views.i18n import JavaScriptCatalog

router = routers.DefaultRouter()
router.register(r'images', api_viewsets.ImageViewSet)
router.register(r'evaluations', api_viewsets.EvaluationViewSet)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
                  path('', IndexView.as_view(), name="index_view"),
                  path(_('users/'), include('studio.urls.user_urls')),
                  path(_('ambitos/'), include('studio.urls.ambit_urls')),
                  path(_('subjects/'), include('studio.urls.subject_urls')),
                  path(_('odas/'), include('studio.urls.oda_urls')),
                  path(_('images/'), include('studio.urls.image_urls')),
                  path(_('momentos/'), include('studio.urls.moment_urls')),
                  path(_('admin/'), admin.site.urls),
                  path(_('api/'), include(router.urls)),
                  path(_('api-auth/'), include('rest_framework.urls', namespace='rest_framework')),
                  path(_('jsi18n/'), JavaScriptCatalog.as_view(), name='javascript-catalog'),
              )
