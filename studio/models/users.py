from django.db import models

from alumnica_entities.users import User, Administrator, ContentCreator, DataAnalyst, Learner


class UserModel(User, models.Model):
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

    name_field = models.CharField(max_length=100, verbose_name='nombre')
    last_name_field = models.CharField(max_length=100, verbose_name='apellido')
    email_field = models.CharField(max_length=250, verbose_name='correo electrónico')
    password_field = models.CharField(max_length=100, verbose_name='contraseña')
    type_field = models.CharField(max_length=20, verbose_name='tipo')

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        abstract = True

    def __str__(self):
        return str(self.name)


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
