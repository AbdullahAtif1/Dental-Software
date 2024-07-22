from django.urls import path
from . import views
from django.urls import include

app_name='blog'

urlpatterns = [
	path('', views.index, name="index"),
	path('<int:article_id>/<slug:slug>/detail/', views.detail, name='detail'),

	# path('tinymce/', include('tinymce.urls')),
	# path('subscribe/', views.subscribe, name='subscribe'),
]

