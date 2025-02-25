import json
import urllib

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from alumnica_model.models.content import Image, Evaluation,Content
from studio.serializers import ContentUploadFileSerializer, ImageHyperlinkedModelSerializer, EvaluationHyperlinkedModelSerializer


class ImageViewSet(ModelViewSet):
    """
    Retrieves Image objects stored in database
    """
    queryset = Image.objects.all()
    serializer_class = ImageHyperlinkedModelSerializer

    def get_queryset(self):
        """
    Gets Image model queryset using filters received in query_params request field
        """
        raw_filter_data = self.request.query_params.get('statuses')
        if raw_filter_data is None:
            return super(ImageViewSet, self).get_queryset(), []

        decoded_filter_data = urllib.parse.unquote(urllib.parse.unquote(raw_filter_data))
        filters = json.loads(decoded_filter_data)

        filter_params = {}
        sort_params = []
        paging_value = None
        current_page = None

        for filter in filters:
            action = filter['action']
            if action == 'filter':
                data = filter['data']['value']
                if data != '':
                    filter_params.update({'folder__contains': data, 'file_name__contains': data})
            elif action == 'paging':

                try:
                    paging = filter['data']['number']
                    if paging != 'all':
                        paging_value = int(paging)
                    else:
                        paging_value = 'all'
                except KeyError or ValueError:
                    pass
                try:
                    current_page = filter['data']['currentPage']
                except KeyError:
                    pass

            elif action == 'sort':
                pass

        if len(filter_params) != 0:
            filter = Q()
            for item in filter_params:
                filter |= Q(**{item: filter_params[item]})

            if paging_value == 'all':
                queryset = Image.objects.filter(filter)
            else:
                queryset = Image.objects.filter(filter)[(paging_value * current_page):
                                                        ((paging_value * current_page) + paging_value)]
            count = len(queryset)

            return queryset, count
        else:
            if paging_value == 'all':
                return \
                    Image.objects.all(), Image.objects.count()
            else:
                return Image.objects.all()[
                       (paging_value * current_page):((paging_value * current_page) + paging_value)], \
                       Image.objects.count()

    def list(self, request, *args, **kwargs):
        self.object_list, count = self.get_queryset()
        serializer = self.get_serializer(self.object_list, many=True)
        return Response({'status': status.HTTP_200_OK, 'count': count, 'data': serializer.data})


class EvaluationViewSet(ModelViewSet):
    """
    Retrieves Evaluation objects
    """
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationHyperlinkedModelSerializer



class ContentUploadAPIView(ModelViewSet):
    """
    Receives H5P file to save
    """
    queryset = Content.objects.all()    
    serializer_class = ContentUploadFileSerializer

    # def post(self, request, version, format=None):

    #         serializer = ContentUploadFileSerializer(data=request.DATA, files=request.FILES)
    #         print (serializer)
    #         if serializer.is_valid():
    #             print ('is valid')
    #             serializer.save()       
    #             return Response(status=status.HTTP_200_OK)
    #         else:
    #             print ('no valid')
    #             return Response(status=status.HTTP_400_BAD_REQUEST)
        

