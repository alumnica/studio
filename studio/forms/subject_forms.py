
from django import forms
from django.core.exceptions import ValidationError

from alumnica_model.models import SubjectModel, TagModel
from alumnica_model.models.content import ImageModel


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

    sections_field = forms.IntegerField(max_value=4)
    subject_field = forms.CharField()
    section1_img = forms.ImageField()
    section2_img = forms.ImageField()
    section3_img = forms.ImageField()

    def clean(self):
        clean_data = super(SubjectSectionsForm, self).clean()
        sections = int(clean_data.get('sections_field'))
        subject_name = clean_data.get('subject_field')
        subject = SubjectModel.objects.get(name_field=subject_name)
        sections_created = subject.number_of_sections
        sections_available_to_create = 4 - sections_created

        if sections_available_to_create == 0:
            error = ValidationError("You can not create more sections in this subject Already has 4.", code='subject_error')
            self.add_error('subject_field', error)

        elif sections_available_to_create < sections:
            error = ValidationError("You can create only %s sections more." % sections_available_to_create, code='subject_error')
            self.add_error('subject_field', error)


    def save_form(self, section_images, subject):
        for name, section_image in section_images:
            image_model, created = ImageModel.objects.get_or_create(name_field=name, file_field=section_image)
            subject.sections_images_field.add(image_model)
        subject.save()

        return subject


