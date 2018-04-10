
from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel, ODAModel


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'number_of_sections_field']

    def clean(self):
        cleaned_data = super(CreateSubjectForm, self).clean()
        name_subject = cleaned_data.get('name_field')

        if SubjectModel.objects.filter(name_field=name_subject).exists():
            error = ValidationError("Subject already exists.", code='subject_error')
            self.add_error('name_field', error)

        ambit = cleaned_data.get('ambit_field')
        if ambit.subjects.count() > 3:
            error = ValidationError("This ambit already has 4 subjects assigned.", code='subject_error')
            self.add_error('name_field', error)

        return cleaned_data

    def save_form(self, user, tags):
        subject = super(CreateSubjectForm, self).save(commit=False)
        subject.created_by = user.profile
        subject.save()
        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            subject.tags_field.add(tag)

        subject.save()
        return subject


class SubjectSectionsForm(forms.Form):

    section1_img = forms.ImageField()
    section2_img = forms.ImageField()
    section3_img = forms.ImageField()

    def save_form(self, section_images, subject):

        for name, section_image in section_images:
            image_model, created = ImageModel.objects.get_or_create(name_field=name, file_field=section_image)
            subject.sections_images_field.add(image_model)
        subject.save()

        return subject


class ODAsSectionForm(forms.Form):
    section_field = forms.CharField()
    oda_name1 = forms.CharField()
    oda_name2 = forms.CharField()
    oda_name3 = forms.CharField()
    oda_name4 = forms.CharField()
    oda_name5 = forms.CharField()
    oda_name6 = forms.CharField()

    oda_image1 = forms.ImageField()
    oda_image2 = forms.ImageField()
    oda_image3 = forms.ImageField()
    oda_image4 = forms.ImageField()
    oda_image5 = forms.ImageField()
    oda_image6 = forms.ImageField()


    def save_form(self, user, subject_name, names_list, images_list):
        subject = SubjectModel.objects.get(name_field=subject_name)
        i = 0

        for name, image in images_list:
            oda_name = names_list[i]
            oda, created = ODAModel.objects.get_or_create(name_field=oda_name, icon_field=image, created_by_field=user.profile, subworld_field=subject)
            i += 1

        subject.save()

        return subject

