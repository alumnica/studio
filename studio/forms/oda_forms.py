from django.core.exceptions import ValidationError
from django import forms

from alumnica_model.models import SubjectModel, ODAModel


class ODAsSectionForm(forms.Form):
    section_field = forms.CharField()
    subject_field = forms.CharField()
    odas_counter = forms.IntegerField(max_value=8)

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


    def clean(self):

        cleaned_data = super(ODAsSectionForm, self).clean()
        section = int(cleaned_data.get('section_field'))
        subject_name = cleaned_data.get('subject_field')
        odas_to_create = int(cleaned_data.get('odas_counter'))
        odas_created = SubjectModel.objects.get(name_field=subject_name).odas.filter(section_field=section).count()
        odas_available_to_create = 8 - odas_created

        if odas_available_to_create == 0:
            error = ValidationError("You can not create more ODAs in this section Already has 8.", code='oda_error')
            self.add_error('section_field', error)

        elif odas_available_to_create < odas_to_create:
            error = ValidationError("You can create only %s ODAs more." % odas_available_to_create, code='oda_error')
            self.add_error('section_field', error)


    def save_form(self, user, subject_name, names_list, images_list, section):
        subject = SubjectModel.objects.get(name_field=subject_name)
        i = 0

        for name, image in images_list:
            oda_name = names_list[i]
            oda, created = ODAModel.objects.get_or_create(name_field=oda_name, icon_field=image, created_by_field=user.profile, subworld_field=subject, section_field=section)
            i += 1

        subject.save()

        return subject


class ODAsPositionForm(forms.Form):
    pass