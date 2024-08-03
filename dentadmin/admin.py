from django.contrib import admin
from .models import *

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'email')
    list_filter = ('status',)


@admin.register(ProspectFile)
class ProspectFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'prospect', 'datetime')
    search_fields = ('title', 'prospect__name')
    list_filter = ('prospect',)
    
