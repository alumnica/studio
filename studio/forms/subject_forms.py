from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field']

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
    def save_form(self, section1_img, section2_img, section3_img, subject_name):
        subject = SubjectModel.objects.get(name=subject_name)
        image_model_1 = ImageModel.objects.get_or_createc(name_field=section1_img.name, file_field=section1_img)
        image_model_2 = ImageModel.objects.get_or_create(name_field=section2_img.name, file_field=section2_img)
        image_model_3 = ImageModel.objects.get_or_create(name_field=section3_img.name, file_field=section3_img)

        subject.sections_images_field.add(image_model_1, image_model_2, image_model_3)
        subject.save()

        return subject

