from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from django_h5p.models import H5Package, H5PLibrary, H5PackageDependency, PreloadedCSS, PreloadedJS, EmbedType


# noinspection PyAbstractClass
class PackageUploadFileSerializer(serializers.Serializer):
    package = serializers.FileField()


# noinspection PyAbstractClass
class JobSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    created_at = serializers.DateTimeField()
    started_at = serializers.DateTimeField()
    enqueued_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField()
    func_name = serializers.CharField(max_length=250)
    is_failed = serializers.BooleanField()
    is_finished = serializers.BooleanField()
    is_queued = serializers.BooleanField()
    is_started = serializers.BooleanField()
    status = serializers.CharField(max_length=50)
    url = serializers.CharField(max_length=50,required=False)


class H5PackageHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = H5Package
        fields = '__all__'


class H5PLibraryHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = H5PLibrary
        fields = '__all__'


class H5PackageDependencyHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = H5PackageDependency
        fields = '__all__'


class PreloadedCSSHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PreloadedCSS
        fields = '__all__'


class PreloadedJSHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PreloadedJS
        fields = '__all__'


class EmbedTypeHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = EmbedType
        fields = '__all__'
