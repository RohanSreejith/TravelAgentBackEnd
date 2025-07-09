from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator

class TravelAgent(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='travel_agent_set',
        related_query_name='travel_agent',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='travel_agent_set',
        related_query_name='travel_agent',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username
    
class Website(models.Model):
    agent = models.ForeignKey(TravelAgent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField(validators=[URLValidator()])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TravelPackage(models.Model):
    agent = models.ForeignKey(TravelAgent, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.destination}"

class ScrapedPackage(models.Model):
    agent = models.ForeignKey(TravelAgent, on_delete=models.CASCADE)
    source_website = models.ForeignKey(Website, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    original_url = models.URLField()
    
    def __str__(self):
        return f"{self.title} from {self.source_website.name}"

class PackageMedia(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    package = models.ForeignKey(TravelPackage, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='package_media/')

    def __str__(self):
        return f"{self.media_type} for {self.package.title}"