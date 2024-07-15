from django.db import models

class Prospect(models.Model):
    STATUS_CHOICES = [
        ('new_buyer', 'New Buyer'),
        ('repeat_customer', 'Repeat Customer'),
    ]

    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='imgs/', blank=True, null=True)
    bio = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class ProspectFile(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/')
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.title


