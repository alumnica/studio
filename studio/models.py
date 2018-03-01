from django.db import models

# Create your models here.
from entities.content_organization.structures import World, Subworld


class WorldModel(World, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def description(self):
        return self.description_field

    @property
    def subworlds(self):
        return self.subworldmodel_set.all()

    name_field = models.CharField(max_length=150, verbose_name='nombre')
    description_field = models.TextField(blank=True, verbose_name='descripción')




class SubworldModel(Subworld, models.Model):
    @property
    def name(self):
        self.name_field

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

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    world_field = models.ForeignKey(WorldModel, on_delete=models.CASCADE, verbose_name='mundo')