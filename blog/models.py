from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.urls import reverse
from django.core.mail import send_mail
from main.models import Subscriber
from main import email_templates
from django.utils.translation import gettext_lazy as _
from concurrent.futures import ThreadPoolExecutor

class Article(models.Model):

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]
    title = models.CharField(_('title'), max_length=100)
    description = models.CharField(_('description'), max_length=1000)
    body = HTMLField(_('body'))
    slug = models.SlugField(_('slug'), blank=True)
    header_image = models.ImageField(_('header image'), upload_to='imgs/', blank=True, null=True)
    pub_date = models.DateField(_('publication date'), auto_now_add=True)
    updated = models.DateField(_('last updated'), auto_now=True)
    status = models.CharField(_('status'), max_length=12, choices=STATUS_CHOICES, default='Draft')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
        # Send emails in a separate thread
        # threading.Thread(target=self.notify_sbscrbrs).start()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.id, 'slug': self.slug})

    def notify_sbscrbrs(self):
        subscribers = Subscriber.objects.all()

        def send_email(subscriber_email):
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

        # Define the number of threads you want in the pool
        num_threads = 10

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit email sending tasks to the pool
            futures = [executor.submit(send_email, subscriber.email) for subscriber in subscribers]

            # Wait for all tasks to complete
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Error sending email: {e}")

        print("All emails sent")
