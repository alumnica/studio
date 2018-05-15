from django.urls import path
from studio.views.ambit_views import *

urlpatterns = [
    path('create_ambit/', CreateAmbitView.as_view(), name='create_ambit_view'),
    path('update_ambit/<int:pk>/', UpdateAmbitView.as_view(), name='update_ambit_view'),
    path('ambits/', AmbitView.as_view(), name='ambits_view'),
    path('delete_ambit/<int:pk>/', DeleteAmbitView.as_view(), name='delete_ambit_view'),
    path('test/', ImagesTestKinichView.as_view(), name='test_view'),
    path('ambits/<int:pk>/', UnPublishAmbitView.as_view(), name='unpublish_ambit_view'),
]
