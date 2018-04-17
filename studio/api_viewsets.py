from rest_framework.viewsets import ModelViewSet

from alumnica_model.models.content import ImageModel
from studio.serializers import ImageHyperlinkedModelSerializer


class ImageViewSet(ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageHyperlinkedModelSerializer

