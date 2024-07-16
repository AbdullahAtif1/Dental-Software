from django.db import models
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import get_user_model
from . import email_templates


# email list for the users to fill their email in for subscribing to newsletters or other promotional stuff
class Subscriber(models.Model):

	email = models.EmailField(unique=True)
	subscribed_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
			return self.email


# Appointment booking functionality displayed on the client side
class Appointment(models.Model):
        
	STATUS_CHOICES = [
			('under_review', 'Under Review'),
			('approved', 'Approved'),
			('not_approved', 'Not Approved'),
	]

	name = models.CharField(max_length=255)
	email = models.EmailField()
	subject = models.CharField(max_length=300)
	description = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)

	# Have to add phone number field for SMS

	def __str__(self):
			return self.subject

	def save(self, *args, **kwargs):
			if self.status == 'under_review':
				self.notify_superuser()
			else:
				self.send_confirmation_email()

			self.add_to_sbscrbr_list()	

			super().save(*args, **kwargs)

	def notify_superuser(self):
			superuser_email = get_user_model().objects.filter(is_superuser=True).values_list('email', flat=True).first()
			if superuser_email:
					
					subject = self.subject
					from_email = "socialcodepk@gmail.com" # Replace with client's gmail account
					to = ["manager@socialcodepk.com"] # Replace with client's official email adress
					body = f"You have a new appointment request from {self.name}. Here's the request details:\n{self.description}"
					reply_to = self.email

					EmailMessage(
						subject,
						body,
						from_email, # Send from (your website)
						to, # Send to (your admin email). Replace afterwards with something like admin@socialcodepk.com
						[], # bcc left empty
						reply_to = reply_to # Email from the form to get back to
					).send(fail_silently=False)
					
	def send_confirmation_email(self):
		if self.status == 'approved':
				message = email_templates.APPOINTMENT_APPROVAL_TEMPLATE.format(
					client_name = self.name,
					appointment_date = self.date,
					appointment_time = self.time,
					company_name = "Amazing Dentals", # Change it afterwards
					your_name = "My Name",
					contact_info = "manager@socialcodepk.com" # Replace with client's official email adress
				)
		else:
				message = email_templates.APPOINTMENT_NOT_APPROVED_TEMPLATE.format(
					client_name = self.name,
					company_name = "Amazing Dentals", # Change it afterwards
					your_name = "My Name",
					contact_info = "manager@socialcodepk.com" # Replace with client's official email adress
				)
		send_mail(
            'Appointment Status Update',
            message,
            "socialcodepk@gmail.com" # From Email. Replace with client's gmail account
            [self.email],
            fail_silently=False,
        )

	def add_to_sbscrbr_list(self):

		if not Subscriber.objects.filter(email=self.email).exists(): # Add the appointment applying person to the mailing list
			subscriber = Subscriber.objects.create(email = self.email)
			subscriber.save(force_insert=True)
		return	


class Feedback(models.Model):
	STARS_CHOICES = [
			(1, '1 Star'),
			(2, '2 Stars'),
			(3, '3 Stars'),
			(4, '4 Stars'),
			(5, '5 Stars'),
	]

	name = models.CharField(max_length=255)
	email = models.EmailField()
	body = models.TextField()
	stars = models.IntegerField(choices=STARS_CHOICES)

	def save(self, *args, **kwargs):

		self.add_to_sbscrbr_list()		
		super().save(*args, **kwargs)

	def __str__(self):
			return f'Feedback from {self.name}'

	def add_to_sbscrbr_list(self):

		if not Subscriber.objects.filter(email=self.email).exists(): # Add the appointment applying person to the mailing list
			subscriber = Subscriber.objects.create(email = self.email)
			subscriber.save(force_insert=True)
		return

