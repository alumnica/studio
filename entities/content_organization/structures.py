from enum import Enum


class World:
    @property
    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def subworlds(self):
        pass


class Subworld:
    @property
    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def theme(self):
        pass

    @property
    def world(self):
        pass

    @property
    def odas(self):
        pass


class ODA:
    @property
    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def icon(self):
        pass

    @property
    def subworld(self):
        pass

    @property
    def micro_odas(self):
        pass

    def is_complete(self):
        pass


class MicroODAType(Enum):
    INTERACTIVE_VIDEO = 'Video Interactivo'
    WIKIRETO = 'WikiReto'
    ENIGMA_COMIC = 'Enigma Comic'
    MINI_JUEGO = 'MiniJuego'
    ORGANIZADOR = 'Organizador'


class MicroODA:
    @property
    def name(self):
        pass

    @property
    def description(self):
        pass

    @property
    def type(self):
        pass

    @property
    def default_position(self):
        pass

    @property
    def learners_progress(self):
        pass

    @property
    def oda(self):
        pass
