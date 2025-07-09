# travel_agent_app/apps.py
from django.apps import AppConfig

class TravelAgentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel_agent_app'

    def ready(self):
        import travel_agent_app.signals  # This line is crucial