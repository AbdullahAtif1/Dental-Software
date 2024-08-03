from django import forms
from .models import Patient, ProspectFile
from phonenumber_field.formfields import PhoneNumberField

class PatientForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = Patient
        fields = ['picture', 'status', 'email', 'phone_number']

class ProspectFileForm(forms.ModelForm):
    class Meta:
        model = ProspectFile
        fields = ['prospect', 'file', 'title', 'description']
