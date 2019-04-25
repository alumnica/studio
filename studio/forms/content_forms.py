# import json
# import logging
# import os
# import tempfile
# import uuid


# from django.contrib.humanize.templatetags import humanize
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm, forms, Form
# from django.template.defaultfilters import filesizeformat
# from django.utils.translation import gettext_lazy as _
# #from rq import Queue
# from storages.backends.s3boto3 import S3Boto3Storage
# from alumnica_model.validators import validate_files
# #from studio_webapp import worker

# _logger = logging.getLogger('studio')


# class ContentForm(Form):
#     """
#     Uploads H5P package
#     """
#     url = forms.URLField(widget=forms.URLInput(attrs={'id': 'h5p-upload-url'}))
#     library = forms.URLField(widget=forms.URLInput(attrs={'id': 'h5p-upload-library'}))
#     content = forms.FileField(validators=[validate_files] widget=forms.FileInput(attrs={'class': 'show-for-sr', 'id': 'content'}))

#     class Meta:
#         model = Moment
#         fields = ['content_type',  'url', 'library', 'content']

#     def __init__(self, *args, **kwargs):
#         super(ContentForm, self).__init__(*args, **kwargs)

#     def save(self):
#         content = self['content']

#         s3 = S3Boto3Storage()

#         s3_filename = os.path.join('temp', str(uuid.uuid4()))
#         with s3.open(s3_filename, 'wb') as s3_file:
#             _logger.debug('Uploading {} to {}'.format(content.name, s3_filename))
#             for chunk in content.chunks(chunk_size=s3_file.buffer_size):
#                 wrote = s3_file.write(chunk)
#                 _logger.debug('Transmitted {} bytes to S3'.format(filesizeformat(wrote)))

#         #q = Queue(connection=worker.conn)
#         return True #q.enqueue(save_h5package, s3_filename, timeout=600)


#     def save_form(self,  moment_type, h5p_id = None):
#         print ('In create moment')

#         cleaned_data = super(MomentCreateForm, self).clean()
#         moment = super(MomentCreateForm, self).save(commit=False)
#         print (moment)
#         tags = cleaned_data.get('tags').split(',')
#         subject = Subject.objects.get(name=subject_name)
#         oda = subject.odas.get(name=oda_name)
#         microoda = oda.microodas.get(type=MicroODAType.objects.get(name=microoda_type))

#         moment.folder = 'Momentos'
#         moment.created_by = user
#         moment.type = moment_type # MomentType.objects.get(name=moment_type)
#         #moment.h5p_package = H5Package.objects.get(job_id=h5p_id)
#         moment.microoda = microoda
#         moment.save()

#         for tag_name in tags:
#             tag, created = Tag.objects.get_or_create(name=tag_name)
#             tag.save()
#             moment.tags.add(tag)

#         moment.save()


    

