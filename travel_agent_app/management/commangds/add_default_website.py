# travel_agent_app/management/commands/add_default_websites.py
from django.core.management.base import BaseCommand
from travel_agent_app.models import TravelAgent, Website

class Command(BaseCommand):
    help = 'Add default websites for all existing users'

    def handle(self, *args, **options):
        for user in TravelAgent.objects.all():
            if not Website.objects.filter(agent=user).exists():
                default_websites = [
                    {'name': 'MakeMyTrip', 'url': 'https://www.makemytrip.com'},
                    {'name': 'Booking.com', 'url': 'https://www.booking.com'},
                    {'name': 'Expedia', 'url': 'https://www.expedia.com'}
                ]
                
                for site in default_websites:
                    Website.objects.create(
                        agent=user,
                        name=site['name'],
                        url=site['url'],
                        is_active=True
                    )
                self.stdout.write(f'Added websites for {user.username}')