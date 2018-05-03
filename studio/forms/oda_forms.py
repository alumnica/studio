from django import forms

from alumnica_model.models import ODAModel
from alumnica_model.models.content import ODAInSubjectModel, ImageModel, SubjectModel, TagModel, MomentModel, \
    MicroODAModel
from alumnica_model.validators import file_size


class ODAModelForm(forms.Form):
    oda_name = forms.CharField(required=True, max_length=120)
    active_icon_field = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                               'type': 'file'}))
    completed_icon_field = forms.ImageField(validators=[file_size], widget=forms.FileInput(attrs={'class': 'is-hidden',
                                                                                                  'type': 'file'}))

    def save_form(self, user, section):
        cleaned_data = self.clean()
        oda_name = cleaned_data.get('oda_name')

        active_image = cleaned_data.get('active_icon_field')
        if ImageModel.objects.all().filter(name_field=active_image.name).exists():
            active_icon = ImageModel.objects.get(name_field=active_image.name)
        else:
            active_icon = ImageModel.objects.create(
                name_field=("oda_{}_section{}_active_icon".format(oda_name, section)), file_field=active_image)

        completed_image = cleaned_data.get('completed_icon_field')
        if ImageModel.objects.all().filter(name_field=completed_image.name).exists():
            completed_icon = ImageModel.objects.get(name_field=completed_image.name)
        else:
            completed_icon = ImageModel.objects.create(
                name_field=("oda_{}_section{}_completed_icon".format(oda_name, section)), file_field=completed_image)

        oda, oda_created = ODAModel.objects.get_or_create(name_field=oda_name, created_by_field=user)

        oda_in_subject, created = ODAInSubjectModel.objects.get_or_create(oda_field=oda, section_field=section,
                                                                          active_icon_field=active_icon,
                                                                          completed_icon_field=completed_icon)
        if not created:
            oda_in_subject.active_icon_field = active_icon
            oda_in_subject.completed_icon_field = completed_icon

        oda_in_subject.save()
        return oda_in_subject


class BaseODAModelFormset(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseODAModelFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ODAsSectionView(forms.ModelForm):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))

    class Meta:
        model = SubjectModel
        fields = ['name_field']


class ODAsPositionForm(forms.Form):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))


class ODAsPreviewForm(forms.Form):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'is-hidden'}))

class ODACreateForm(forms.ModelForm):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))
    class Meta:
        model = ODAModel
        fields = ['name_field']

    def save_form(self, user, tags, moments):
        oda = super(ODACreateForm, self).save(commit=False)
        oda.created_by_field = user.profile
        oda.save()
        if tags is not None:
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = TagModel.objects.get_or_create(name_field=tag_name)
                oda.tags_field.add(tag)
        counter = 1
        for moment_object in moments:

            if moment_object[1] is not None:

                moments_names = moment_object[1].split(',')
                microoda, created = MicroODAModel.objects.get_or_create(name_field='{}_{}'.format(oda.name, moment_object[0]),
                                                               created_by_field=user.profile, type_field=moment_object[0],
                                                      default_position_field=counter, oda_field=oda)
                counter += 1

                for moment_name in moments_names:
                    moment = MomentModel.objects.get(name_field=moment_name)
                    microoda.activities_field.add(moment)
                    microoda.save()

        oda.save()
        return oda

class ODAUpdateForm(forms.ModelForm):
    name_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'oda-name'}))
    class Meta:
        model = ODAModel
        fields = ['name_field']

    def save_form(self,user, tags, moments):
        oda = super(ODAUpdateForm, self).save(commit=False)
        if tags is not None:
            tags = tags.split(',')
            for tag_name in tags:
                tag, created = TagModel.objects.get_or_create(name_field=tag_name)
                oda.tags_field.add(tag)
        counter = 0
        for moment_object in moments:

            if moment_object[1] is not None:

                moments_names = moment_object[1].split(',')

                try:
                    microoda = MicroODAModel.objects.get(name_field='{}_{}'.format(oda.name, moment_object[0]),
                                                      type_field=moment_object[0], oda_field=oda)
                except MicroODAModel.DoesNotExist:
                    microoda = MicroODAModel.objects.create(name_field='{}_{}'.format(oda.name, moment_object[0]),
                                                         type_field=moment_object[0], created_by_field=user.profile,
                                                            oda_field=oda)

                for moment_name in moments_names:
                    moment = MomentModel.objects.get(name_field=moment_name)
                    microoda.activities_field.add(moment)
                    microoda.save()

                for moment in microoda.activities_field.all():
                    if moment.name_field not in moments_names:
                        microoda.activities_field.remove(moment)
                    microoda.save()
        oda.save()

        return oda