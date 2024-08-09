from django.urls import path
from . import views

app_name='main'

urlpatterns = [
	path('', views.index, name="index"),
	path('logout/', views.custom_logout, name='logout'),
	path('signup/', views.sigunp, name="signup")
]
