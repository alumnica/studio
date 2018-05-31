from rest_framework.serializers import HyperlinkedModelSerializer

from alumnica_model.models.content import Image


class ImageHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
