from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Patient(models.Model):

	STATUS_CHOICES = [
			('new_buyer', 'New Buyer'),
			('repeat_customer', 'Repeat Customer'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.ImageField(upload_to='imgs/', blank=True, null=True)
	bio = models.TextField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new_buyer')
	email = models.EmailField()
	phone_number = PhoneNumberField()

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
        Patient, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.title
