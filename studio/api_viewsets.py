import json
import urllib

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from alumnica_model.models.content import Image
from studio.serializers import ImageHyperlinkedModelSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageHyperlinkedModelSerializer

    def get_queryset(self):
        raw_filter_data = self.request.query_params.get('statuses')
        if raw_filter_data is None:
            return super(ImageViewSet, self).get_queryset()

        decoded_filter_data = urllib.parse.unquote(urllib.parse.unquote(raw_filter_data))
        filters = json.loads(decoded_filter_data)

        filter_params = {}
        sort_params = []
        paging_value = ''
        paging = 1

        for filter in filters:
            action = filter['action']
            if action == 'filter':
                data = filter['data']['value']
                if data != '':
                    filter_params.update({'folder_contains': data, 'file_name_contains': data})
            elif action == 'paging':
                data = filter['data']['number']
                if data != '':
                    paging_value = filter['data']['number']
            elif action == 'sort':
                pass

        x = len(filter_params)
        if len(filter_params) != 0:
            filter = Q()
            for item in filter_params:
                filter |= Q(**{item: filter_params[item]})

            queryset = Image.objects.filter(filter)
            count = len(queryset)

            return queryset, count
        else:
            return Image.objects.all(), Image.objects.count()

    def list(self, request, *args, **kwargs):
        self.object_list, count = self.get_queryset()
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'status': status.HTTP_200_OK, 'count': count, 'data': serializer.data})
