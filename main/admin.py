from django.contrib import admin
from .models import *

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'date', 'time')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('status', 'date', 'time')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'stars', 'body')
    list_filter = ('stars',)
    search_fields = ('name', 'email')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


