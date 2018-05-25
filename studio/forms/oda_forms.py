
from django import forms

from alumnica_model.models import ODA
from alumnica_model.models.content import Subject, Tag, Moment, \
    MicroODA


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
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))

    class Meta:
        model = ODA
        fields = ['name', 'tags', 'active_icon', 'completed_icon']

    def save_form(self, user, tags, moments, is_draft=False):

        oda = super(ODACreateForm, self).save(commit=False)
        cleaned_data = super(ODACreateForm, self).clean()
        oda.created_by = user
        oda.temporal = is_draft
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
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': ''}))

    class Meta:
        model = ODA
        fields = ['name', 'tags', 'active_icon', 'completed_icon']

    def save_form(self, user, tags, moments, is_draft=False):
        cleaned_data = super(ODAUpdateForm, self).clean()
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
        oda.temporal = is_draft
        oda.save()

        return oda
