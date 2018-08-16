import rq
from django.http import Http404
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from alumnica_model.models.h5p import H5Package, H5PLibrary, H5PackageDependency, PreloadedCSS, PreloadedJS, EmbedType
from django_h5p.forms import H5PackageForm
from django_h5p.serializers import H5PackageHyperlinkedModelSerializer, H5PLibraryHyperlinkedModelSerializer, \
    H5PackageDependencyHyperlinkedModelSerializer, PreloadedCSSHyperlinkedModelSerializer, \
    PreloadedJSHyperlinkedModelSerializer, EmbedTypeHyperlinkedModelSerializer, PackageUploadFileSerializer, \
    JobSerializer
from studio_webapp import worker


class PackageUploadAPIView(APIView):
    serializer_class = PackageUploadFileSerializer

    def post(self, request, *args, **kwargs):
        """
Receives H5p package
        """
        form = H5PackageForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            return Response({
                'status': 'success', 'job': {
                    'id': job.id,
                    'package_job_id': '{}'.format(job.id),
                    'job_url': '{}://{}{}'.format(
                        request.scheme,
                        request.get_host(),
                        reverse_lazy('job_detail_view', kwargs={'job_id': job.id})
                    )
                }})
        else:
            return Response({'status': 'error', 'error': form.errors.as_text()})


class JobAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
Gets current job id
        """
        q = rq.Queue(connection=worker.conn)
        job = q.fetch_job(job_id=kwargs.get('job_id'))
        if job:
            return Response(JobSerializer(job).data)
        else:
            raise Http404()


class H5PackageViewSet(ModelViewSet):
    serializer_class = H5PackageHyperlinkedModelSerializer
    queryset = H5Package.objects.all()


class H5PLibraryViewSet(ModelViewSet):
    serializer_class = H5PLibraryHyperlinkedModelSerializer
    queryset = H5PLibrary.objects.all()


class H5PackageDependencyViewSet(ModelViewSet):
    serializer_class = H5PackageDependencyHyperlinkedModelSerializer
    queryset = H5PackageDependency.objects.all()


class PreloadedCSSViewSet(ModelViewSet):
    serializer_class = PreloadedCSSHyperlinkedModelSerializer
    queryset = PreloadedCSS.objects.all()


class PreloadedJSViewSet(ModelViewSet):
    serializer_class = PreloadedJSHyperlinkedModelSerializer
    queryset = PreloadedJS.objects.all()


class EmbedTypeViewSet(ModelViewSet):
    serializer_class = EmbedTypeHyperlinkedModelSerializer
    queryset = EmbedType.objects.all()
