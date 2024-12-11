from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from .models import Subject, Lesson


class EnrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.student_subjects.all()
        )
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'), Submit('enroll', 'Enroll', css_class='mt-2 mb2')
        )


class UnenrollForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = user.student_subjects.all()

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'), Submit('unenroll', 'Unenroll', css_class='mt-2 mb-2 btn btn-danger')
        )


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')
        required = ('title',)

    title = forms.CharField()
    content = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            Submit(
                'add_lesson',
                'Add Lesson',
                css_class='mt-2 btn btn-primary',
            ),
        )

    def save(self, subject, *args, **kwargs):
        lesson = super().save(commit=False)
        lesson.subject = subject
        lesson = super().save(*args, **kwargs)
        return lesson
