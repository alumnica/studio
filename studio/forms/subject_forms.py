from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel, ODAModel


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

    def save_form(self, section_images, subject):

        for section_image in section_images:
            image_model = ImageModel.objects.get_or_create(name_field=section_image.name, file_field=section_image)
            subject.sections_images_field.add(image_model)
        subject.save()

        return subject


class ODAsSectionForm(forms.Form):

    def save_form(self, user, subject_name, names_list, images_list):
        subject = SubjectModel.objects.get(name=subject_name)

        for i in range(0, len(names_list)):
            image = images_list[i]
            image_model = ImageModel.objects.get_or_create(name_field=image.name, file_field=image)
            oda = ODAModel.objects.get_or_create(name_field= names_list[i], icon_field=image_model)
            oda.created_by = user
            oda.save()
            subject.odas_field.add(oda)

        subject.save()

        return subject

