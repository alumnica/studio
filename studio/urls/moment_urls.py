from django.urls import path

from studio.views.moment_views import MomentsView, CreateMomentView

urlpatterns = [
    path('', MomentsView.as_view(), name='momentos_view'),
    path('create', CreateMomentView.as_view(), name='create_momentos_view'),
]
