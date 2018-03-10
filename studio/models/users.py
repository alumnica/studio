from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from alumnica_entities.users import UserEntity, Administrator, ContentCreator, DataAnalyst, Learner


class UserModel(UserEntity,models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def last_name(self):
        return self.last_name_field

    @property
    def email(self):
        return self.email_field

    @property
    def password(self):
        return self.password_field

    @property
    def type(self):
        return self.type_field

    auth_user_field=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')
    type_field = models.CharField(max_length=20, verbose_name='tipo')



    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'


    def __str__(self):
        return str(self.name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserModel.objects.create(auth_user_field=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class AdministratorModel(Administrator, models.Model):

    @property
    def name(self):
        return self.name_field

    @property
    def last_name(self):
        return self.last_name_field

    @property
    def email(self):
        return self.email_field

    @property
    def password(self):
        return self.password_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')

    class Meta:
        verbose_name = 'administrador'
        verbose_name_plural = 'administradores'

    def __str__(self):
        return str(self.name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AdministratorModel.objects.create(auth_user_field=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class ContentCreatorModel(ContentCreator, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def last_name(self):
        return self.last_name_field

    @property
    def email(self):
        return self.email_field

    @property
    def password(self):
        return self.password_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')

    class Meta:
        verbose_name = 'creador de contenidos'
        verbose_name_plural = 'creadores de contenido'

    def __str__(self):
        return str(self.name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ContentCreatorModel.objects.create(auth_user_field=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class DataAnalystModel(DataAnalyst, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def last_name(self):
        return self.last_name_field

    @property
    def email(self):
        return self.email_field

    @property
    def password(self):
        return self.password_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')

    class Meta:
        verbose_name = 'analista de datos'
        verbose_name_plural = 'analistas de datos'

    def __str__(self):
        return str(self.name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            DataAnalystModel.objects.create(auth_user_field=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class LearnerModel(Learner, models.Model):
    @property
    def name(self):
        return self.name_field

    @property
    def last_name(self):
        return self.last_name_field

    @property
    def email(self):
        return self.email_field

    @property
    def password(self):
        return self.password_field

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')

    class Meta:
        verbose_name = 'alumno'
        verbose_name_plural = 'alumnos'

    def __str__(self):
        return str(self.name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            LearnerModel.objects.create(auth_user_field=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
