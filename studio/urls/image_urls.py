from django.urls import path

from studio.views.image_views import ImageLibraryView

urlpatterns = [
    path('library/', ImageLibraryView.as_view(), name='library_view'),
]
