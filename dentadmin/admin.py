from django.contrib import admin
from .models import *

from parler.admin import TranslatableAdmin

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'email')
    list_filter = ('status',)


class ProspectFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'prospect', 'datetime')
    search_fields = ('title', 'prospect__name')
    list_filter = ('prospect',)
    


admin.site.register(Patient, TranslatableAdmin)
admin.site.register(ProspectFile, TranslatableAdmin)