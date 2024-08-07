from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from parler.utils.context import switch_language
from django.utils.translation import get_language
from django.urls import reverse
from django.core.mail import send_mail
from main.models import Subscriber
from main import email_templates
from django.utils.translation import gettext_lazy as _
import threading
from parler.models import TranslatableModel, TranslatedFields

class Article(TranslatableModel):
	STATUS_CHOICES = [
			('Draft', 'Draft'),
			('Published', 'Published'),
	]
	
	header_image = models.ImageField(upload_to='imgs/', blank=True, null=True)
	pub_date=models.DateField(auto_now_add=True)
	updated=models.DateField(auto_now=True)
	slug=models.SlugField(blank=True)
	status = models.CharField(_('status'), max_length=12, choices=STATUS_CHOICES, default='Draft')

	translations = TranslatedFields(
			title=models.CharField(max_length=100),
			description=models.TextField(),
			body=HTMLField(),
	)

	def __str__(self):
			return self.title

	def save(self, *args, **kwargs):
			current_language = get_language()
			with switch_language(self, current_language):
					translated_title = self.safe_translation_getter('title', default='')

			if translated_title:
					self.slug = slugify(translated_title)
			else:
					self.slug = slugify(self.title)  # Fallback to original title if translation is not available

			print(f"Generated slug: {self.slug}")

			super().save(*args, **kwargs)
			print("Article saved, calling notify_sbscrbrs...")
			self.notify_sbscrbrs()

	def get_absolute_url(self):
			return reverse('blog:detail', kwargs={'article_id': self.id, 'slug': self.slug})

	def notify_sbscrbrs(self):
			subscribers = Subscriber.objects.all()
			
			# List to keep track of threads
			threads = []
			
			# Create and start a thread for each subscriber
			for sbscrbr in subscribers:
					thread = threading.Thread(target=self.send_email, args=(sbscrbr.email,))
					thread.start()
					threads.append(thread)

	def send_email(self, subscriber_email):
			message = email_templates.NEW_ARTICLE_TEMPLATE.format(
					article_url=self.get_absolute_url(),
					article_title=self.title,
					company_name="Amazing Dentals",
					your_name="My Name",
					contact_info="manager@socialcodepk.com"
			)
			send_mail(
					f'{self.title} - Amazing Dentals',
					message,
					"socialcodepk@gmail.com",
					[subscriber_email],
					fail_silently=False,
			)
			print("Email sent")

