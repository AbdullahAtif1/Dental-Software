from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="index"),

		path('<str:name>/', views.trgt_index, name="trgt_index"),

    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/signup/', views.sigunp, name="signup"),
    path('accounts/password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("accounts/", include("django.contrib.auth.urls")),
		
		path('<str:name>/contact-us/', views.contact_us_page, name="contact_us_page"),

		# Without name
		path('contact/', views.contact_us_page, name="contact_page"),
]
