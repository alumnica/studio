from abc import ABC

from entities.content_organization.structures import MicroODA
from entities.progress import LearnerProgressInMicroODA


class InteractiveVideo(MicroODA):
    @property
    def root_video_node(self):
        pass


class InteractiveVideoNode:
    @property
    def name(self):
        pass

    @property
    def type(self):
        pass

    @property
    def interactive_video(self):
        pass


class VideoNode(InteractiveVideoNode):
    @property
    def source(self):
        pass

    @property
    def close_captions(self):
        pass

    @property
    def duration_in_seconds(self):
        pass


class ForkNode(InteractiveVideoNode):
    @property
    def image(self):
        pass

    @property
    def selected_link(self):
        pass

    @property
    def available_links(self):
        pass


class NodeLink:
    @property
    def background_image(self):
        pass

    @property
    def target_node(self):
        pass

    @property
    def fork_node(self):
        pass


class ExerciseNode(InteractiveVideoNode, ABC):
    @property
    def exercise(self):
        pass


class LearnerProgressInInteractiveVideo(LearnerProgressInMicroODA):
    @property
    def interactive_video(self):
        pass

    @property
    def current_interactive_video_node(self):
        pass

    @property
    def exercise_solution(self):
        pass
