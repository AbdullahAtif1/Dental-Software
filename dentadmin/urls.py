from django.urls import path
from . import views

app_name='dentadmin'

urlpatterns = [
	path('', views.index, name="index"),
]