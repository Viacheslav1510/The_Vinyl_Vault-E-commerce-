# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
# Internal:
from .models import Contact
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ContactForm(forms.ModelForm):
    """
    A class to create contact form
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': ('+353123456789')}))

    class Meta:
        model = Contact
        fields = (
            'name',
            'phone',
            'email',
            'message')
