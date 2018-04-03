from django import forms

from alumnica_model.models import SubjectModel, TagModel


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'description_field', 'tags_field']

    def save_form(self, user, tags):
        subject = super(CreateSubjectForm, self).save(commit=False)
        subject.created_by = user

        for tagName in tags:
            tag_model = TagModel.objects.get(name=tagName)
            if not tag_model is None:
                tag_model = TagModel.objects.create(name=tagName, ambit=subject)
                subject.tags.add(tag_model)

        subject.save()

class SubjectForm(forms.ModelForm):
    class Meta:
        model = SubjectModel
        fields = ['name_field', 'ambit_field', 'description_field', 'created_at_field', 'tags_field']