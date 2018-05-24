import os

from django import forms

from alumnica_model.models import ODA
from alumnica_model.models.content import Image, Subject, Tag, Moment, \
    MicroODA
from alumnica_model.validators import file_size


class ODAForm(forms.Form):
    oda_name = forms.CharField(required=True, max_length=120)
    active_icon = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                         'type': 'file'}))
    completed_icon = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                            'type': 'file'}))

    def save_form(self, user, section):
        cleaned_data = self.clean()
        oda_name = cleaned_data.get('oda_name')

        active_image = cleaned_data.get('active_icon')
        if isinstance(active_image, Image):
            active_icon = Image.objects.get(folder=active_image.folder,
                                            file=active_image.file)
            active_icon.name = '{}-oda_active_icon'.format(oda_name)
            active_icon.save()
        else:
            active_icon = Image.objects.create(name='{}-oda_active_icon'.format(oda_name),
                                               folder="odas", file=active_image)

            active_icon.file_name = os.path.basename(active_icon.file.name)
            active_icon.save()

        completed_image = cleaned_data.get('completed_icon')
        if isinstance(completed_image, Image):
            completed_icon = Image.objects.get(folder=completed_image.folder,
                                               file=completed_image.file)
            completed_icon.name = '{}-oda_completed_icon'.format(oda_name)
            completed_icon.save()
        else:
            completed_icon = Image.objects.create(name='{}-oda_completed_icon'.format(oda_name),
                                                  folder="odas", file=completed_image)

            completed_icon.file_name = os.path.basename(active_icon.file.name)
            completed_icon.save()

        oda, created = ODA.objects.get_or_create(name=oda_name, created_by=user, section=section,
                                                                     active_icon=active_icon,
                                                                     completed_icon=completed_icon)

        if not created:
            oda.active_icon = active_icon
            oda.completed_icon = completed_icon

        oda.save()
        return oda


class BaseODAFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseODAFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ODAsSectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))

    class Meta:
        model = Subject
        fields = ['name']


class ODAsPositionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODAsPreviewForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODACreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))

    class Meta:
        model = ODA
        fields = ['name']

    def save_form(self, user, tags, moments):
        oda = super(ODACreateForm, self).save(commit=False)
        oda.created_by = user
        oda.save()
        if tags is not None:
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                oda.tags.add(tag)
        counter = 1
        for moment_object in moments:

            if moment_object[1] is not None:

                moments_names = moment_object[1].split(',')
                microoda, created = MicroODA.objects.get_or_create(name='odas',
                                                                   created_by=user,
                                                                   type=moment_object[0],
                                                                   default_position=counter, oda=oda)
                counter += 1

                for moment_name in moments_names:
                    moment = Moment.objects.get(name=moment_name)
                    microoda.activities.add(moment)
                    microoda.save()

        oda.save()
        return oda


class ODAUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))

    class Meta:
        model = ODA
        fields = ['name']

    def save_form(self, user, tags, moments):
        oda = super(ODAUpdateForm, self).save(commit=False)

        if tags is not None:
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                oda.tags.add(tag)

        for moment_object in moments:

            if moment_object[1] is not '' or None:

                moments_names = moment_object[1].split(',')

                try:
                    microoda = MicroODA.objects.get(name='odas', type=moment_object[0], oda=oda)
                except MicroODA.DoesNotExist:
                    microoda = MicroODA.objects.create(name='odas', type=moment_object[0],
                                                       created_by=user, oda=oda)

                for moment_name in moments_names:
                    moment = Moment.objects.get(name=moment_name)
                    microoda.activities.add(moment)
                    microoda.save()

                for moment in microoda.activities.all():
                    if moment.name not in moments_names:
                        microoda.activities.remove(moment)
                    microoda.save()
        oda.save()

        return oda
