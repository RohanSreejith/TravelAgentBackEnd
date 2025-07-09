# travel_agent_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Website, TravelAgent

@receiver(post_save, sender=TravelAgent)
def create_default_websites(sender, instance, created, **kwargs):
    if created and not Website.objects.filter(agent=instance).exists():
        default_websites = [
            {'name': 'MakeMyTrip', 'url': 'https://www.makemytrip.com'},
            {'name': 'Booking.com', 'url': 'https://www.booking.com'},
            {'name': 'Expedia', 'url': 'https://www.expedia.com'},
            {'name': 'Agoda', 'url': 'https://www.agoda.com'},
            {'name': 'TripAdvisor', 'url': 'https://www.tripadvisor.com'}
        ]
        
        for site in default_websites:
            Website.objects.create(
                agent=instance,
                name=site['name'],
                url=site['url'],
                is_active=True
            )