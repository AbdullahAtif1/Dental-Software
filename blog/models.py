from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.mail import send_mail
from main.models import Subscriber
from main import email_templates

class Article(models.Model):

	STATUS_CHOICES = [
			('Draft', 'Draft'),
			('Published', 'Published'),
	]
	title = models.CharField(max_length=1000)
	description = models.CharField(max_length=1000)
	body = models.TextField()
	slug = models.SlugField(blank=True)
	header_image = models.ImageField(upload_to='imgs/', blank=True, null=True)
	pub_date = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	status = models.CharField(
			max_length=12, choices=STATUS_CHOICES, default='Draft')

	def __str__(self):
			return self.title

	def save(self, *args, **kwargs):
			self.slug = slugify(self.title)
			# self.notify_sbscrbrs()

			super(Article, self).save(*args, **kwargs)

	def get_absolute_url(self):
			return reverse('blog:detail', kwargs={'article_id': self.id, 'slug': self.slug})

	def notify_sbscrbrs(self):

		ppl = Subscriber.objects.all()
		for x in ppl:
			message = email_templates.NEW_ARTICLE_TEMPLATE.format(
					client_name = x.name,
					article_url = self.get_absolute_url(),
					article_title = self.title,
					company_name = "Amazing Dentals", # Change it afterwards
					your_name = "My Name",
					contact_info = "manager@socialcodepk.com" # Replace with client's official email adress
				)
			send_mail(
            'Appointment Status Update',
            message,
            "socialcodepk@gmail.com" # From Email. Replace with client's gmail account
            [x.email],
            fail_silently=False,
        )


