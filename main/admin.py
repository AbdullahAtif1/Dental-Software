from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError

from parler.admin import TranslatableAdmin

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'patient', 'status', 'date', 'time')
    list_filter = ('status', 'date')
    search_fields = ('subject', 'patient__name')

    def save_model(self, request, obj, form, change):
        if obj.status == 'approved' and (obj.date is None or obj.time is None):
            raise ValidationError("Date and Time must be set when approving an appointment.")
        super().save_model(request, obj, form, change)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'stars', 'body')
    list_filter = ('stars',)
    search_fields = ('name', 'email')

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

admin.site.register(Appointment, TranslatableAdmin)
admin.site.register(Feedback, TranslatableAdmin)
admin.site.register(Subscriber, TranslatableAdmin)

