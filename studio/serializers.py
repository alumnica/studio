from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from alumnica_model.models.content import Image, Evaluation, Content


class ImageHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class EvaluationHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'



class ContentUploadFileSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

