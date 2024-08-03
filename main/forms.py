from django import forms
from .models import *

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['subject', 'description']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['body', 'stars']

