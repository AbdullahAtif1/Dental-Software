from django import forms
from .models import Prospect, ProspectFile

class ProspectForm(forms.ModelForm):
    class Meta:
        model = Prospect
        fields = ['name', 'picture', 'bio', 'status']

class ProspectFileForm(forms.ModelForm):
    class Meta:
        model = ProspectFile
        fields = ['prospect', 'file', 'title', 'description']
