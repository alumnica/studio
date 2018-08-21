import json
import logging
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile

import rq
# noinspection PyPackageRequirements
from storages.backends.s3boto3 import S3Boto3Storage

from alumnica_model.models.h5p import EmbedType, PreloadedJS, PreloadedCSS, H5PLibrary, H5PackageDependency, H5Package
from studio_webapp import worker

_logger = logging.getLogger('django_h5p')

_s3 = S3Boto3Storage()


def save_h5package(aws_package_name):
    """
Opens H5p package and saves the content
    """
    with ThreadPoolExecutor() as executor:
        futures = []
        with tempfile.NamedTemporaryFile('w+b') as downloaded_file:
            with _s3.open(aws_package_name, 'rb') as s3_file:
                downloaded_file.write(s3_file.read())
                downloaded_file.flush()

            _s3.delete(aws_package_name)

            with tempfile.TemporaryDirectory() as package:
                with ZipFile(downloaded_file) as zip_root:
                    zip_root.extractall(path=package)

                with open(os.path.join(package, 'h5p.json')) as h5p_json_file:
                    h5p_json = json.load(h5p_json_file)

                main_library = h5p_json['mainLibrary']
                preloaded_dependencies = h5p_json['preloadedDependencies']
                index = [x for x in preloaded_dependencies if x['machineName'] == main_library]

                for dep in preloaded_dependencies:
                    _save_package_dependency(package, dep, futures, executor)

                if not H5PLibrary.objects.filter(machine_name__exact=main_library).exists():
                    _logger.info(
                        "{} doesn't exist in database. Checking if it's included in package...".format(main_library))
                    _save_library(package, main_library, futures, executor)

                for dep in preloaded_dependencies:
                    if not H5PLibrary.objects.filter(
                            machine_name__exact=dep['machineName'],
                            major_version=int(dep['majorVersion']),
                            minor_version=int(dep['minorVersion'])
                    ).exists():
                        _logger.info("{} doesn't exist in database. Checking if it's included in package...".format(
                            main_library))
                        _save_library(package, dep['machineName'], futures, executor)

                with open(os.path.join(package, 'content', 'content.json'), encoding='utf-8') as content_json_file:
                    h5p = H5Package.objects.create(
                        title=h5p_json['title'],
                        language=h5p_json['language'],
                        content=content_json_file.read().replace('#tmp', '').replace('\n', ''),
                        main_library=H5PLibrary.objects.filter(
                            machine_name__exact=main_library,
                            major_version=int(index[0]['majorVersion']),
                            minor_version=int(index[0]['minorVersion'])).order_by(
                            '-patch_version'
                        ).first(),
                        job_id=rq.get_current_job(worker.conn).id
                    )

                for embed_type in h5p_json['embedTypes']:
                    embed, created = EmbedType.objects.get_or_create(type=embed_type)
                    h5p.embed_types.add(embed)

                h5p.save()

                for x in preloaded_dependencies:
                    H5PackageDependency.objects.create(
                        package=h5p,
                        library=H5PLibrary.objects.filter(
                            machine_name=x['machineName'],
                            major_version=x['majorVersion'],
                            minor_version=x['minorVersion']
                        ).order_by('-patch_version').first(),
                    )

                package_content_dir = os.path.join(package, 'content')

                _upload_directory_to_aws(h5p.pk, package_content_dir, futures, executor, path_prefix='content')


def _save_package_dependency(package, dependency, futures, executor):
    """
Gets package dependencies
    """
    machine_name = dependency['machineName']
    major_version = dependency['majorVersion']
    minor_version = dependency['minorVersion']
    library_full_name = '{}-{}.{}'.format(machine_name, major_version, minor_version)
    library_directory = os.path.join(package, library_full_name)

    if not os.path.exists(library_directory):
        _logger.error('Library directory for {} does not exist in the package'.format(library_full_name))

    if 'library.json' in os.listdir(library_directory):
        _logger.info('Library {} found'.format(library_full_name))
        _save_library(package, library_full_name, futures, executor)


def _save_library(root_dir, library, futures, executor):
    """
Creates library object in H5PLibrary table
    """
    library_filename = [x for x in os.listdir(root_dir) if x.startswith(library)][0]
    library_dir = os.path.join(root_dir, library_filename)
    library_json_file = os.path.join(library_dir, 'library.json')

    with open(library_json_file, encoding='utf8') as file:
        library_json = json.load(file)

        library, created = H5PLibrary.objects.update_or_create(
            title=library_json['title'],
            description=library_json.get('description'),
            major_version=library_json['majorVersion'],
            minor_version=library_json['minorVersion'],
            patch_version=library_json['patchVersion'],
            runnable=library_json['runnable'],
            author=library_json.get('author'),
            license=library_json.get('license'),
            machine_name=library_json['machineName'],
            fullscreen=library_json.get('fullscreen', False)
        )

        library.embed_types.set([
            EmbedType.objects.get_or_create(type=x)[0] for x in library_json.get('embedTypes', [])
        ])

        library.preloaded_js.set(
            [PreloadedJS.objects.create(path=x['path'], library=library) for x in library_json.get('preloadedJs', [])])

        library.preloaded_css.set(
            [PreloadedCSS.objects.create(path=x['path'], library=library) for x in library_json.get('preloadedCss', [])]
        )

        for dep in library_json.get('preloadedDependencies', []):
            dep_filename = [x for x in os.listdir(root_dir) if x.startswith(dep['machineName'])][0]
            _logger.debug('Saving dependency for {} -> {}'.format(library_filename, dep_filename))
            _save_library(root_dir, dep_filename, futures, executor)

            lib = H5PLibrary.objects.filter(
                machine_name=dep['machineName'],
                major_version=dep['majorVersion'],
                minor_version=dep['minorVersion']
            ).order_by('-patch_version').first()

            library.preloaded_dependencies.add(lib)

    _upload_directory_to_aws(library.full_name_no_spaces, library_dir, futures, executor, path_prefix='libraries')

    return library


def _upload_directory_to_aws(content_id, directory_to_upload, futures, executor, path_prefix=''):
    """
    Uploads content to AWS
    """
    for current_dir, _, filenames in os.walk(directory_to_upload):
        relative_path_to_root_dir = os.path.relpath(current_dir, directory_to_upload)
        for file in filenames:
            futures.append(
                executor.submit(ble, current_dir, file, path_prefix, content_id, relative_path_to_root_dir)
            )


def ble(current_dir, file, path_prefix, content_id, relative_path_to_root_dir):
    f = os.path.join(current_dir, file)
    with open(f, 'rb') as local_file:
        file_path_in_aws = os.path.join(
            path_prefix,
            str(content_id),
            relative_path_to_root_dir if relative_path_to_root_dir != '.' else '',
            file
        )

        _logger.info('Uploading {} to {}'.format(local_file.name, file_path_in_aws))
        remote_file = _s3.open(file_path_in_aws, 'wb')
        remote_file.write(local_file.read())
        remote_file.close()
