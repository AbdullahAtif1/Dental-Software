from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

class Patient(TranslatableModel):
	STATUS_CHOICES = [
			('new_buyer', 'New Buyer'),
			('repeat_customer', 'Repeat Customer'),
	]
	
	email = models.EmailField()
	phone_number = PhoneNumberField()
	status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='new_buyer')
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
	picture = models.ImageField(upload_to='imgs/', blank=True, null=True)

	translations = TranslatedFields(
			bio=models.TextField(null=True, blank=True),
	)

	@receiver(post_save, sender=User)
	def create_or_update_user_profile(sender, instance, created, **kwargs):
			if created:
					# Create a new Patient instance when a User is created
					Patient.objects.create(user=instance, email=instance.email)
			else:
					# Update the email of the existing Patient instance
					instance.patient.email = instance.email
					instance.patient.save()

	# Get the phone number from the signup form, it'll include patient form with fields, image, phone number, bio

	def __str__(self):
			return self.user.username


class ProspectFile(models.Model):

	prospect = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='files', verbose_name=_('prospect'))
	file = models.FileField(upload_to='files/')
	datetime = models.DateTimeField(auto_now_add=True)
	title=models.CharField(max_length=255, verbose_name=_('title'))
	description=models.TextField(verbose_name=_('description'))
	
	def __str__(self):
			return self.title
