import json
import os
import zipfile
from zipfile import ZipFile

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_is_h5p(package):
    filename, file_extension = os.path.splitext(str(package))

    if file_extension != '.h5p':
        raise ValidationError(
            _("The file must have a .h5p extension. {extension} given".format(extension=file_extension)),
            code='invalid_extension')

    if not zipfile.is_zipfile(package):
        raise ValidationError(_("The file isn't a ZIP file"), code='not_zip')

    with ZipFile(package) as h5p_root:
        filenames = [x.filename for x in h5p_root.filelist]

        if 'h5p.json' not in filenames:
            raise ValidationError(_('The package is missing the "h5p.json" file in its root level'),
                                  code='h5p_json_missing')

        try:
            h5p_json = json.load(h5p_root.open('h5p.json'))
            validate_h5p_json(h5p_json)
        except json.JSONDecodeError as e:
            raise ValidationError(_('Invalid JSON format in h5p.json file. Error: {error}'.format(error=e.msg)),
                                  code='invalid_h5p_json_format')


def validate_h5p_json(h5p_json):
    required_fields = [
        'title',
        'mainLibrary',
        'language',
        'preloadedDependencies',
        'embedTypes'
    ]

    missing_fields = set(required_fields).symmetric_difference(h5p_json.keys())

    if len(missing_fields) > 0:
        raise ValidationError(_('The following required fields are missing in the "h5p.json" file: '
                                '{fields}'.format(fields=missing_fields)), code='missing_h5p_json_fields')


def validate_h5p_library(library_directory):
    if not any(x == 'library.json' for x in os.listdir(library_directory)):
        raise ValidationError(_("Library {} doesn't contain a 'library.json' file"), code='missing_library_json')

    with open(os.path.join(library_directory, 'library.json')) as library_json_file:
        try:
            library_json = json.load(library_json_file)
        except json.JSONDecodeError as e:
            raise ValidationError(_('Invalid JSON format in "library.json" file. Error: {error}'.format(error=e.msg)),
                                  code='invalid_library_json_format')

        validate_library_json(library_json)
        validate_library_files(
            [x['path'] for x in library_json.get('preloadedJs', [])],
            [x['path'] for x in library_json.get('preloadedCss', [])],
            library_directory
        )


def validate_library_json(library_json_data):
    if library_json_data['title'].isspace():
        raise ValidationError(_('Empty library title'), code='invalid_title')

    if any('path' not in x.keys() for x in library_json_data.get('preloadedJs', [])):
        raise ValidationError(_('A member of the preloaded JavaScripts does not have the "path" attribute'),
                              code='invalid_library_json_format')

    if any('path' not in x.keys() for x in library_json_data.get('preloadedCss', [])):
        raise ValidationError(_('A member of the preloaded CSS does not have the "path" attribute'),
                              code='invalid_library_json_format')


def validate_library_files(preloaded_js, preloaded_css, library_directory):
    missing_files = []
    missing_files.extend([x for x in preloaded_js if not os.path.exists(os.path.join(library_directory, x))])
    missing_files.extend([x for x in preloaded_css if not os.path.exists(os.path.join(library_directory, x))])

    if len(missing_files) > 0:
        raise ValidationError(
            _("The following files are needed but aren't part of the package. {}".format(
                ', '.join(missing_files))), code='missing_files')
