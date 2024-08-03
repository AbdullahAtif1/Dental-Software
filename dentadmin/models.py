from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):

	STATUS_CHOICES = [
			('new_buyer', 'New Buyer'),
			('repeat_customer', 'Repeat Customer'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
	picture = models.ImageField(upload_to='imgs/', blank=True, null=True, verbose_name=_('profile picture'))
	bio = models.TextField(null=True, blank=True, verbose_name=_('bio'))
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new_buyer', verbose_name=_('status'))
	email = models.EmailField(verbose_name=_('email address'))
	phone_number = PhoneNumberField(verbose_name=_('phone number'))

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Patient.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.patient.save()

	def __str__(self):
			return self.user.first_name


# Replace the prospect model with "Patient" user model

class ProspectFile(models.Model):
    prospect = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='files', verbose_name=_('prospect'))
    file = models.FileField(upload_to='files/', verbose_name=_('file'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('date and time'))
    description = models.TextField(verbose_name=_('description'))

    def __str__(self):
        return self.title
