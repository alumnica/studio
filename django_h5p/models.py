from collections import OrderedDict

from django.db import models


class H5Package(models.Model):
    title = models.CharField(max_length=150)
    main_library = models.ForeignKey('H5PLibrary', on_delete=models.CASCADE, related_name='dependent_packages')
    language = models.CharField(max_length=10)
    preloaded_dependencies = models.ManyToManyField('H5PLibrary', through='H5PackageDependency')
    embed_types = models.ManyToManyField('EmbedType', related_name='dependent_packages')
    content_type = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=150, null=True, blank=True)
    license = models.CharField(max_length=50, null=True, blank=True)
    dynamic_dependencies = models.ManyToManyField('H5PLibrary', related_name='required_dynamically_by_packages')
    metakeywords = models.CharField(max_length=150, null=True, blank=True)
    metadescription = models.TextField(null=True, blank=True)
    job_id = models.CharField(max_length=36, null=True, blank=True)


class H5PLibrary(models.Model):
    """
    H5P Library definition according to the library.json specification.
    https://h5p.org/library-definition
    """
    title = models.CharField(max_length=50)
    machine_name = models.CharField(max_length=150)
    major_version = models.PositiveSmallIntegerField()
    minor_version = models.PositiveSmallIntegerField()
    patch_version = models.PositiveSmallIntegerField()
    runnable = models.BooleanField()
    coreapi_major_version = models.PositiveSmallIntegerField(null=True, blank=True)
    coreapi_minor_version = models.PositiveSmallIntegerField(null=True, blank=True)
    author = models.CharField(max_length=250, null=True, blank=True)
    license = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    preloaded_dependencies = models.ManyToManyField('H5PLibrary', related_name='required_preloaded_by_libraries')
    dynamic_dependencies = models.ManyToManyField('H5PLibrary', related_name='required_dynamically_by_libraries')
    embed_types = models.ManyToManyField('EmbedType', related_name='dependent_libraries')
    fullscreen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('machine_name', 'major_version', 'minor_version', 'patch_version')

    @property
    def full_name(self):
        return '{} {}.{}'.format(self.machine_name, self.major_version, self.minor_version)

    @property
    def full_name_no_spaces(self):
        return '{}-{}.{}'.format(self.machine_name, self.major_version, self.minor_version)

    def __str__(self):
        return self.full_name

    def get_all_stylesheets(self, css=None):
        entry_level = False

        if css is None:
            entry_level = True
            css = []

        for dep in self.preloaded_dependencies.all():
            css.extend(dep.get_all_stylesheets(css))

        css.extend([
            'https://s3.amazonaws.com/django-h5p-dev/libraries/{}/{}'.format(self.full_name_no_spaces, css.path)
            for css in self.preloaded_css.all().order_by('pk')
        ])

        return list(OrderedDict.fromkeys(css)) if entry_level else css

    def get_all_javascripts(self, js=None):
        entry_level = False

        if js is None:
            entry_level = True
            js = []

        for dep in self.preloaded_dependencies.all():
            js.extend(dep.get_all_javascripts(js))

        js.extend(
            'https://s3.amazonaws.com/django-h5p-dev/libraries/{}/{}'.format(self.full_name_no_spaces, script.path)
            for script in self.preloaded_js.all().order_by('pk')
        )

        return list(OrderedDict.fromkeys(js)) if entry_level else js


class H5PackageDependency(models.Model):
    package = models.ForeignKey(H5Package, on_delete=models.CASCADE)
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pk']


class PreloadedCSS(models.Model):
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE, related_name='preloaded_css')
    path = models.CharField(max_length=255)


class PreloadedJS(models.Model):
    library = models.ForeignKey(H5PLibrary, on_delete=models.CASCADE, related_name='preloaded_js')
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.path


class EmbedType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type
