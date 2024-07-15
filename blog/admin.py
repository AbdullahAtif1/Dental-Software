from django.contrib import admin
from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'updated', 'status']
	list_filter = ('title', 'pub_date')
	list_editable = ['status']
    


