import json
import urllib

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from alumnica_model.models.content import ImageModel
from studio.serializers import ImageHyperlinkedModelSerializer

class ImageViewSet(ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageHyperlinkedModelSerializer

    def get_queryset(self):
        filter = json.loads(urllib.parse.unquote(urllib.parse.unquote(self.request.query_params.get('statuses'))))[0]['data']['value']
        return ImageModel.objects.filter(name_field__startswith=filter)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


