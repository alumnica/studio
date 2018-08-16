import json
import logging
import os
import tempfile
import uuid
from zipfile import ZipFile

from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms, Form
from django.utils.translation import gettext_lazy as _
from rq import Queue
from storages.backends.s3boto3 import S3Boto3Storage

from alumnica_model.models.h5p import H5PLibrary
from django_h5p.saver import save_h5package
from django_h5p.validators import validate_is_h5p, validate_h5p_library
from studio_webapp import worker

_logger = logging.getLogger('django_h5p')


class H5PackageForm(Form):
    package = forms.FileField(validators=[validate_is_h5p])

    def __init__(self, *args, **kwargs):
        super(H5PackageForm, self).__init__(*args, **kwargs)

    def save(self):
        """
Saves H5P package
        """
        uploaded_package = self.cleaned_data['package']

        s3 = S3Boto3Storage()

        s3_filename = os.path.join('temp', str(uuid.uuid4()))
        with s3.open(s3_filename, 'wb') as s3_file:
            for chunk in uploaded_package.chunks():
                s3_file.write(chunk)

        q = Queue(connection=worker.conn)
        return q.enqueue(save_h5package, s3_filename, timeout=600)

    def clean(self):
        """
Verifies  whether package or database contains libraries needed
        """
        cleaned_data = super(H5PackageForm, self).clean()

        if 'package' not in cleaned_data.keys():
            return

        with tempfile.TemporaryDirectory() as temp_dir:
            with ZipFile(cleaned_data['package']) as h5p_root:
                h5p_root.extractall(path=temp_dir)

            with open(os.path.join(temp_dir, 'h5p.json')) as h5p_json_file:
                h5p_json = json.load(h5p_json_file)

                main_library = h5p_json['mainLibrary']
                preloaded_dependencies = h5p_json['preloadedDependencies']

                if not H5PLibrary.objects.filter(machine_name__exact=main_library).exists():
                    _logger.info(
                        "{} doesn't exist in database. Checking if it's included in package...".format(main_library))
                    self._check_if_library_exists_in_zip(temp_dir, main_library)

                for dep in preloaded_dependencies:
                    if not H5PLibrary.objects.filter(machine_name__exact=dep['machineName'],
                                                     major_version=int(dep['majorVersion']),
                                                     minor_version=int(dep['minorVersion'])).exists():
                        _logger.info("{} doesn't exist in database. Checking if it's included in package...".format(
                            main_library))
                        self._check_if_library_exists_in_zip(temp_dir, dep['machineName'])

                for library in [x for x in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, x))]:
                    library_dir = os.path.join(temp_dir, library)
                    if any(x == 'library.json' for x in os.listdir(library_dir)):
                        _logger.info('Library {} found'.format(library))
                        validate_h5p_library(library_dir)

        return cleaned_data

    @staticmethod
    def _check_if_library_exists_in_zip(zip_root, library):
        """
Looks up for the libraries in the H5p package
        """
        if not any(x.startswith(library) for x in os.listdir(zip_root)):
            raise ValidationError(_("Main library {} hasn't been loaded and isn't included in package.".format(
                library
            )), code='missing_library')


class H5PLibraryModelForm(ModelForm):
    class Meta:
        model = H5PLibrary
        fields = '__all__'
