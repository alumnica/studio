import os

from django import forms

from alumnica_model.models import Ambit
from alumnica_model.models.content import Tag, Subject, Image, Program, Badge
from alumnica_model.validators import unique_ambit_name_validator, file_size, validate_image_extension


class CreateAmbitForm(forms.ModelForm):
    """
    Create new Ambito form
    """
    name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}),
                           validators=[unique_ambit_name_validator])

    ap = forms.ImageField(required=False, validators=[file_size, validate_image_extension], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))

    aU = forms.ImageField(required=False, validators=[file_size, validate_image_extension],
                               widget=forms.FileInput(attrs={'id': 'aUpload',
                                                                         'class': 'is-hidden',
                                                                         'type': 'file'}))
    bU = forms.ImageField(required=False, validators=[file_size, validate_image_extension],
                                            widget=forms.FileInput(attrs={'id': 'bUpload',
                                                                          'class': 'is-hidden',
                                                                          'type': 'file'}))
    cU = forms.ImageField(required=False, validators=[file_size, validate_image_extension],
                                           widget=forms.FileInput(attrs={'id': 'cUpload',
                                                                         'class': 'is-hidden',
                                                                         'type': 'file'}))

    class Meta:
        model = Ambit
        fields = ['name']

    def save_form(self, user, subjects, tags, color):
        """
        Creates new ambito in database as not temporal object
        :param user: Current AuthUser creating the object
        :param subjects: Subjects string separated by comma
        :param tags: Tags array
        :param color: Background color
        """
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.color = color

        #Badge creation
        badge_first_version = cleaned_data.get('aU')
        badge_second_version = cleaned_data.get('bU')
        badge_third_version = cleaned_data.get('cU')
        if badge_first_version is not None:
            badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                 file=badge_first_version)
        else:
            badge_image_1 = None
        if badge_second_version is not None:
            badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                 file=badge_second_version)
        else:
            badge_image_2 = None
        if badge_third_version is not None:
            badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                 file=badge_third_version)
        else:
            badge_image_3 = None

        ambit.badge = Badge.objects.create(name=ambit.name, first_version=badge_image_1, second_version=badge_image_2, third_version=badge_image_3)

        image = cleaned_data.get('ap')
        if isinstance(image, Image):
            image_model = Image.objects.get(folder="Ambitos", file=image.file)
            image_model.name = '{}-ambit_image'.format(ambit.name)
            image_model.save()
        else:
            image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                               folder="Ambitos", file=image)

        image_model.file_name = os.path.basename(image_model.file.name)
        image_model.save()
        ambit.background_image = image_model
        ambit.program = Program.objects.get(name="Primaria")
        ambit.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = False
            tag.save()
            ambit.tags.add(tag)

        if subjects is not None:
            subjects = subjects.split('|')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        all_subjects_finalized = True
        for subject in ambit.subjects.all():
            if subject.temporal:
                all_subjects_finalized = False
                break

        ambit.is_draft = not all_subjects_finalized
        ambit.is_published = False
        if ambit.position == 0:
            ambit.position = Ambit.objects.all().count()
        ambit.save()

        return ambit, all_subjects_finalized

    def save_as_draft(self, user, subjects, tags, color):
        """
        Creates new ambito in database as temporal object
        :param user: Current AuthUser creating the object
        :param subjects: Subjects string separated by comma
        :param tags: Tags array
        :param color: Background color
        """
        cleaned_data = super(CreateAmbitForm, self).clean()
        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user
        ambit.program = Program.objects.get(name="Primaria")
        ambit.color = color

        # Badge creation
        badge_first_version = cleaned_data.get('aU')
        badge_second_version = cleaned_data.get('bU')
        badge_third_version = cleaned_data.get('cU')

        if ambit.badge is None:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
            else:
                badge_image_1 = None
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
            else:
                badge_image_2 = None
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
            else:
                badge_image_3 = None
            ambit.badge = Badge.objects.create(name=ambit.name, first_version=badge_image_1, second_version=badge_image_2,
                                           third_version=badge_image_3)
        else:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
                ambit.badge.first_version = badge_image_1
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
                ambit.badge.second_version = badge_image_2
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
                ambit.badge.third_version = badge_image_3
        ambit.badge.save()

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="Ambitos", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="Ambitos", file=image)

            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()

            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags.add(tag)

        if subjects is not None:
            subjects = subjects.split('|')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass

        ambit.save()


class UpdateAmbitForm(forms.ModelForm):
    """
    Update existing Ambito object form
    """
    name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'text_number'}))

    ap = forms.ImageField(required=False, validators=[validate_image_extension], widget=forms.FileInput(attrs={'name': 'ap',
                                                                                                'id': 'ambito-u',
                                                                                                'class': 'is-hidden',
                                                                                                'type': 'file'}))
    aU = forms.ImageField(required=False, validators=[validate_image_extension],
                                           widget=forms.FileInput(attrs={'id': 'aUpload',
                                                                         'class': 'is-hidden',
                                                                         'type': 'file'}))
    bU = forms.ImageField(required=False, validators=[validate_image_extension],
                                            widget=forms.FileInput(attrs={'id': 'bUpload',
                                                                          'class': 'is-hidden',
                                                                          'type': 'file'}))
    cU = forms.ImageField(required=False, validators=[validate_image_extension],
                                           widget=forms.FileInput(attrs={'id': 'cUpload',
                                                                         'class': 'is-hidden',
                                                                         'type': 'file'}))

    class Meta:
        model = Ambit
        fields = ['name']

    def save_form(self, subjects, tags, color, pk):
        """
        Updates ambit properties and saves it as not temporal object
        :param subjects: Subjects string separated by comma
        :param tags: Tags array
        :param color: Background color
        """
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = Ambit.objects.get(pk=pk)
        ambit.color = color
        ambit.name = cleaned_data.get('name')
        image = cleaned_data.get('ap')

        # Badge creation
        badge_first_version = cleaned_data.get('aU')
        badge_second_version = cleaned_data.get('bU')
        badge_third_version = cleaned_data.get('cU')

        if ambit.badge is None:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
            else:
                badge_image_1 = None
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
            else:
                badge_image_2 = None
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
            else:
                badge_image_3 = None
            ambit.badge = Badge.objects.create(name=ambit.name, first_version=badge_image_1,
                                               second_version=badge_image_2,
                                               third_version=badge_image_3)
        else:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
                ambit.badge.first_version = badge_image_1
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
                ambit.badge.second_version = badge_image_2
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
                ambit.badge.third_version = badge_image_3
        ambit.badge.save()

        if image is not None:
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="Ambitos", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="Ambitos", file=image)
            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()
            image_model.save()
            ambit.background_image = image_model
        ambit.save()

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if tag not in ambit.tags.all():
                ambit.tags.add(tag)
        for tag in ambit.tags.all():
            if tag.name not in tags:
                ambit.tags.remove(tag)

        if subjects is not None:
            subjects = subjects.split('|')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        for subject in ambit.subjects.all():
            if subject.name not in subjects:
                ambit.subjects.remove(subject)

        all_subjects_finalized = True
        for subject in ambit.subjects.all():
            if subject.temporal:
                all_subjects_finalized = False
                break

        ambit.is_draft = not all_subjects_finalized
        ambit.is_published = False
        if ambit.position == 0:
            ambit.position = Ambit.objects.all().count()
        ambit.save()

        return ambit, all_subjects_finalized

    def save_as_draft(self, subjects, tags, color, pk):
        """
        Updates ambit properties and saves it as temporal object
        :param subjects: Subjects as string separated by comma
        :param tags: Tags array
        :param color: Background color
        """
        cleaned_data = super(UpdateAmbitForm, self).clean()
        ambit = Ambit.objects.get(pk=pk)
        ambit.color = color
        ambit.name = cleaned_data.get('name')

        # Badge creation
        badge_first_version = cleaned_data.get('aU')
        badge_second_version = cleaned_data.get('bU')
        badge_third_version = cleaned_data.get('cU')

        if ambit.badge is None:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
            else:
                badge_image_1 = None
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
            else:
                badge_image_2 = None
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
            else:
                badge_image_3 = None
            ambit.badge = Badge.objects.create(name=ambit.name, first_version=badge_image_1,
                                               second_version=badge_image_2,
                                               third_version=badge_image_3)
        else:
            if badge_first_version is not None:
                badge_image_1 = Image.objects.create(name='{}_badge_first_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_first_version)
                ambit.badge.first_version = badge_image_1
            if badge_second_version is not None:
                badge_image_2 = Image.objects.create(name='{}_badge_second_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_second_version)
                ambit.badge.second_version = badge_image_2
            if badge_third_version is not None:
                badge_image_3 = Image.objects.create(name='{}_badge_third_image'.format(ambit.name), folder="Ambitos",
                                                     file=badge_third_version)
                ambit.badge.third_version = badge_image_3
        ambit.badge.save()

        if cleaned_data.get('ap') is not None:
            image = cleaned_data.get('ap')
            if isinstance(image, Image):
                image_model = Image.objects.get(folder="Ambitos", file=image.file)
                image_model.name = '{}-ambit_image'.format(ambit.name)
                image_model.save()
            else:
                image_model = Image.objects.create(name='{}-ambit_image'.format(ambit.name),
                                                   folder="Ambitos", file=image)

            image_model.file_name = os.path.basename(image_model.file.name)
            image_model.save()
            ambit.background_image = image_model
        ambit.save()
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)

            tag.temporal = True
            tag.save()
            ambit.tags.add(tag)
        for tag in ambit.tags.all():
            if tag.name not in tags:
                ambit.tags.remove(tag)

        if subjects is not None:
            subjects = subjects.split('|')
            for subject_name in subjects:
                try:
                    subject_model = Subject.objects.get(name=subject_name)
                    ambit.subjects.add(subject_model)
                except Subject.DoesNotExist:
                    pass
        for subject in ambit.subjects.all():
            if subject.name not in subjects:
                ambit.subjects.remove(subject)
        ambit.is_draft = True
        ambit.save()
