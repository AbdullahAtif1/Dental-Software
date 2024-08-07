from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Subscriber, Appointment, Feedback

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email',]  # This should be 'email' as a TranslatableField
        labels = {
            'email': _("Email Address"),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('subject', 'description')
        labels = {
            'subject': _("Subject"),
            'description': _("Description"),
        }

class FeedbackForm(forms.Form):
    class Meta:
        model = Feedback
        fields = ['body', 'stars']
        labels = {
            'body': _("Feedback"),
            'stars': _("Rating"),
        }
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

