from django.urls import path

from studio.views.moment_views import MomentsView

urlpatterns = [
    path('', MomentsView.as_view(), name='momentos_view'),
]
