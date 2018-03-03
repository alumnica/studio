from abc import ABCMeta

from django.db import models


class ABCAMetaAndModelBase(ABCMeta, models.base.ModelBase):
    """
    Metaclass for classes that inherit from ABC and models.Model.
    """
    pass
