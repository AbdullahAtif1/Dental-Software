from django import forms
from .models import Patient, ProspectFile
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class PatientForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = Patient
        fields = ['picture', 'status', 'email', 'phone_number']
        labels = {
            'picture': _("Profile Picture"),
            'status': _("Status"),
            'email': _("Email Address"),
            'phone_number': _("Phone Number"),
        }

class ProspectFileForm(forms.ModelForm):
    class Meta:
        model = ProspectFile
        fields = ['prospect', 'file', 'title', 'description']
        labels = {
            'prospect': _("Prospect"),
            'file': _("File"),
            'title': _("Title"),
            'description': _("Description"),
        }
