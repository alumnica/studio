from abc import ABC, abstractmethod

from content_organization.structures import MicroODA
from progress import LearnerProgressInMicroODA


class InteractiveVideo(MicroODA, ABC):
    @property
    @abstractmethod
    def root_video_node(self):
        pass


class InteractiveVideoNode(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def interactive_video(self):
        pass


class VideoNode(InteractiveVideoNode, ABC):
    @property
    @abstractmethod
    def source(self):
        pass

    @property
    @abstractmethod
    def close_captions(self):
        pass

    @property
    @abstractmethod
    def duration_in_seconds(self):
        pass


class ForkNode(InteractiveVideoNode, ABC):
    @property
    @abstractmethod
    def image(self):
        pass

    @property
    @abstractmethod
    def selected_link(self):
        pass

    @property
    @abstractmethod
    def available_links(self):
        pass


class NodeLink(ABC):
    @property
    @abstractmethod
    def background_image(self):
        pass

    @property
    @abstractmethod
    def target_node(self):
        pass

    @property
    @abstractmethod
    def fork_node(self):
        pass


class ExerciseNode(InteractiveVideoNode, ABC):
    @property
    @abstractmethod
    def exercise(self):
        pass


class LearnerProgressInInteractiveVideo(LearnerProgressInMicroODA, ABC):
    @property
    @abstractmethod
    def interactive_video(self):
        pass

    @property
    @abstractmethod
    def current_interactive_video_node(self):
        pass

    @property
    @abstractmethod
    def exercise_solution(self):
        pass
