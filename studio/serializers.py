from rest_framework.serializers import HyperlinkedModelSerializer

from alumnica_model.models.content import ImageModel


class ImageHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'
