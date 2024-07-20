from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
	path('', views.index, name="index"),
	path('<int:article_id>/<slug:slug>/detail/', views.detail, name='detail'),
	# path('subscribe/', views.subscribe, name='subscribe'),
]

