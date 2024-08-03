from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin

# @admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'updated', 'status']
	list_filter = ('title', 'pub_date')
	list_editable = ['status']
    
admin.site.register(Article, TranslatableAdmin)

