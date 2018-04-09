from django.urls import path
from studio.views.ambit_views import *

urlpatterns = [
    path('create_ambit/', CreateAmbitView.as_view(), name='create_ambit_view'),
    path('ambits/', AmbitView.as_view(), name='ambits_view'),
]
