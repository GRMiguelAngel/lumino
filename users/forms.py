from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')

    avatar = forms.ImageField()
    bio = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            Field('avatar'),
            Field('bio'),
            Submit(
                'edit_profile',
                'Guardar cambios',
                css_class='mt-2 btn btn-primary',
            ),
        )
