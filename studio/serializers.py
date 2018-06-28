from rest_framework.serializers import HyperlinkedModelSerializer

from alumnica_model.models.content import Image, Evaluation


class ImageHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class EvaluationHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
