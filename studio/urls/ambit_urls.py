from django.urls import path

from studio.views.ambit_views import CreateAmbitView, UpdateAmbitView, AmbitView, DeleteAmbitView, UnPublishAmbitView

urlpatterns = [
    path('', AmbitView.as_view(), name='ambits_view'),
    path('create_ambit/', CreateAmbitView.as_view(), name='create_ambit_view'),
    path('update_ambit/<int:pk>/', UpdateAmbitView.as_view(), name='update_ambit_view'),
    path('delete_ambit/<int:pk>/', DeleteAmbitView.as_view(), name='delete_ambit_view'),
    path('ambits/<int:pk>/', UnPublishAmbitView.as_view(), name='unpublish_ambit_view'),
]
