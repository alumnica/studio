import json
import os
import shutil
import tempfile

from django.core.exceptions import ValidationError
from django.test import TestCase

from django_h5p.validators import validate_is_h5p


class H5PackageValidatorTestCase(TestCase):
    def test_h5package_is_zip(self):
        with tempfile.NamedTemporaryFile(suffix='.h5p') as not_a_zip_file:
            try:
                validate_is_h5p(not_a_zip_file.name)
            except ValidationError as e:
                self.assertEqual(e.code, 'not_zip',
                                 "'not_zip' validation error expected when uploading anything other than a zip file.'")

    def test_h5package_has_h5p_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            dir_with_zip_extension = shutil.make_archive(temp_dir, 'zip', temp_dir)

            try:
                validate_is_h5p(dir_with_zip_extension)
            except ValidationError as e:
                expected_error_code = 'invalid_extension'
                self.assertEqual(e.code, expected_error_code,
                                 "'{}' validation error expected when uploading a ZIP file with an extension other than"
                                 " .h5p.".format(expected_error_code))
            finally:
                os.remove(dir_with_zip_extension)

    def test_h5package_has_h5p_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zipped_dir = shutil.make_archive(temp_dir, 'zip', temp_dir)
            filename, file_extension = os.path.splitext(zipped_dir)

            h5p_package = filename + '.h5p'
            os.rename(zipped_dir, h5p_package)

            try:
                validate_is_h5p(h5p_package)
            except ValidationError as e:
                self.assertEqual(e.code, 'h5p_json_missing',
                                 "'h5p_json_missing' validation error expected when uploading a h5p file with no "
                                 "h5p.json file present in the root directory.")
            finally:
                os.remove(h5p_package)

    def test_h5package_with_invalid_h5p_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, 'h5p.json'), mode='w') as h5p_json_file:
                h5p_json_file.write('This is not JSON')

            zipped_dir = shutil.make_archive(temp_dir, 'zip', temp_dir)
            filename, file_extension = os.path.splitext(zipped_dir)

            h5p_package = filename + '.h5p'
            os.rename(zipped_dir, h5p_package)

            try:
                validate_is_h5p(h5p_package)
            except ValidationError as e:
                expected_error_code = 'invalid_h5p_json_format'
                self.assertEqual(e.code, expected_error_code, "'{}' validation error expected when the h5p.json format "
                                                              "isn't a valid JSON".format(expected_error_code))
            finally:
                os.remove(h5p_package)

    def test_h5p_json_file_has_required_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            required_fields = {
                'title': None,
                'mainLibrary': None,
                'language': None,
                'preloadedDependencies': None,
                'embedTypes': None
            }

            for excluded_field in required_fields.keys():
                remaining_fields = {
                    x: required_fields[x] for x in required_fields if x != excluded_field
                }

                with open(os.path.join(temp_dir, 'h5p.json'), mode='w') as h5p_json_file:
                    json.dump(remaining_fields, h5p_json_file)

                self._zip_and_validate_directory(temp_dir)

    def _zip_and_validate_directory(self, temp_dir):
        zipped_dir = shutil.make_archive(temp_dir, 'zip', temp_dir)
        filename, file_extension = os.path.splitext(zipped_dir)
        h5p_package = filename + '.h5p'
        os.rename(zipped_dir, h5p_package)
        try:
            validate_is_h5p(h5p_package)
        except ValidationError as e:
            expected_error_code = 'missing_h5p_json_fields'
            self.assertEqual(e.code, expected_error_code,
                             "'{}' validation error expected when uploading a ZIP file with an extension other than"
                             " .h5p.".format(expected_error_code))
        finally:
            os.remove(h5p_package)
