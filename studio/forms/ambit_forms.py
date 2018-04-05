from django import forms
from django.core.files.storage import default_storage
from django.core.validators import RegexValidator

from alumnica_model.models import AmbitModel
from alumnica_model.models.content import TagModel, SubjectModel, ImageModel, ProgramModel
from studio.validators import unique_ambit_name_validator


class CreateAmbitForm(forms.ModelForm):
    name_field = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'text_number'}),
                                 validators=[unique_ambit_name_validator])
    position_field = forms.IntegerField(max_value=30)

    class Meta:
        model = AmbitModel
        fields = ['name_field', 'position_field']

    def save_form(self, user, subjects, tags, color, image):

        ambit = super(CreateAmbitForm, self).save(commit=False)
        ambit.created_by = user.profile
        ambit.color = color

        if image is not None:
            with default_storage.open(image.name, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            image_model = ImageModel.objects.create(name_field=image.name, file_field=image.name)
            ambit.background_image = image_model
            ambit.program = ProgramModel.objects.get(name_field="Primaria")
            ambit.save()

        for tag_name in tags:
            tag, created = TagModel.objects.get_or_create(name_field=tag_name)
            # tag.ambits_field.add(ambit)
            ambit.tags_field.add(tag)

        if subjects is not None:
            subjects = subjects.split(',')
            for subject_name in subjects:
                try:
                    subject_model = SubjectModel.objects.get(name_field=subject_name)
                    ambit.subjects_field.add(subject_model)
                except SubjectModel.DoesNotExist:
                    pass

        ambit.save()

