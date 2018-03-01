from django.db import models

from entities.content_organization.structures import MicroODAType
from entities.microodas.interactive_video import InteractiveVideo, InteractiveVideoNode, VideoNode, NodeLink, \
    InteractiveVideoNodeType
from studio.models import MicroODAModel


class InteractiveVideoModel(MicroODAModel, InteractiveVideo, models.Model):
    @property
    def root_video_node(self):
        return None

    @property
    def type(self):
        return MicroODAType.INTERACTIVE_VIDEO


class InteractiveVideoNodeModel(InteractiveVideoNode, models.Model):
    NODE_TYPES = (
        (InteractiveVideoNodeType.VIDEO.value, InteractiveVideoNodeType.VIDEO.value),
        (InteractiveVideoNodeType.FORK.value, InteractiveVideoNodeType.FORK.value),
        (InteractiveVideoNodeType.EXERCISE.value, InteractiveVideoNodeType.EXERCISE.value),
    )

    @property
    def name(self):
        return self.name_field

    @property
    def type(self):
        return self.type_field

    @property
    def interactive_video(self):
        return self.interactive_video_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    type_field = models.CharField(max_length=50, choices=NODE_TYPES,
                                  verbose_name='tipo de nodo')
    interactive_video_field = models.ForeignKey(InteractiveVideoModel, on_delete=models.CASCADE,
                                                verbose_name='video interactivo')

    class Meta:
        verbose_name = 'nodo de video interactivo'
        verbose_name_plural = 'nodos de video interactivo'
        abstract = True

    def __str__(self):
        return str(self.name)


class VideoNodeModel(InteractiveVideoNodeModel, VideoNode):
    @property
    def source(self):
        return self.source_field

    @property
    def close_captions(self):
        return self.close_captions_field

    @property
    def duration_in_seconds(self):
        return self.duration_in_seconds_field

    source_field = models.URLField(verbose_name='URL')
    close_captions_field = models.TextField(blank=True, verbose_name='subtítulos')
    duration_in_seconds_field = models.PositiveSmallIntegerField(default=0, verbose_name='duración en segundos')

    class Meta:
        verbose_name = 'nodo de video para Video Interactivo'
        verbose_name_plural = 'nodos de video para Video Interactivo'


class ForkNodeModel(InteractiveVideoNodeModel, VideoNode):
    @property
    def image(self):
        return self.image_field

    @property
    def selected_link(self):
        return self.selected_link_field

    @property
    def available_links(self):
        return self.available_links_set.all()

    image_field = models.ImageField(verbose_name='imagen de fondo')
    selected_link_field = models.ForeignKey('NodeLinkModel', on_delete=models.SET_NULL, null=True, blank=True,
                                            verbose_name='nodo elegido')

    class Meta:
        verbose_name = 'nodo de bifurcación para Video Interactivo'
        verbose_name_plural = 'nodos de bifurcación para Video Interactivo'


class NodeLinkModel(NodeLink, models.Model):
    @property
    def background_image(self):
        return self.background_image_field

    @property
    def target_node(self):
        return self.target_node_field

    @property
    def fork_node(self):
        return self.fork_node_field

    background_image_field = models.ImageField(verbose_name='imagen de fondo')
    fork_node_field = models.ForeignKey(ForkNodeModel, on_delete=models.CASCADE, related_name='available_links_set',
                                        verbose_name='nodo de bifurcación')
    target_node_field = models.ForeignKey(ForkNodeModel, on_delete=models.CASCADE, related_name='incoming_links_set',
                                          verbose_name='siguiente nodo')

    class Meta:
        verbose_name = 'enlace de nodos'
        verbose_name_plural = 'enlaces de nodos'

    def __str__(self):
        return '{} -> {}'.format(self.fork_node_field.name, self.target_node_field.name)

# class ExerciseNodeModel(InteractiveVideoNodeModel, ExerciseNode):
#     @property
#     def exercise(self):
#         return self.exercise_field
#
#     exercise_field = models.ForeignKey(ExerciseModel, on_delete=models.PROTECT, verbose_name='ejercicio')


# class LearnerProgressInInteractiveVideo(LearnerProgressInMicroODA):
#     @property
#     def interactive_video(self):
#         pass
#
#     @property
#     def current_interactive_video_node(self):
#         pass
#
#     @property
#     def exercise_solution(self):
#         pass
