from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Row, Submit
from django import forms

from .models import Enrollment, Lesson, Subject


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


class EditLessonForm(forms.ModelForm):
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
                'edit_lesson',
                'Guardar cambios',
                css_class='mt-2 btn btn-primary',
            ),
        )


class EditMarksForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('mark',)

        mark = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            Field('mark'),
            Submit(
                'edit_mark',
                'Guardar cambios',
                css_class='mt-2 btn btn-primary',
            ),
        )


class EditMarksFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-2">{% student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))
