from django.contrib import admin
from .models import Patient, ProspectFile
from parler.admin import TranslatableAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)		

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'email')
    list_filter = ('status',)

@admin.register(ProspectFile)
class ProspectFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'prospect', 'datetime')
    search_fields = ('title', 'prospect__name')
    list_filter = ('prospect',)
