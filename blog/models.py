from django.db import models
from django.utils.text import slugify

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
			super(Article, self).save(*args, **kwargs)

