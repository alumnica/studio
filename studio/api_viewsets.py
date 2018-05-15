from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from alumnica_model.models.content import ImageModel
from studio.serializers import ImageHyperlinkedModelSerializer


class ImageViewSet(ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageHyperlinkedModelSerializer

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


