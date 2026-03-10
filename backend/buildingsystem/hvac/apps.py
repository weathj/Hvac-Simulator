from django.apps import AppConfig


class HvacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hvac'

    def ready(self):
        from hvac.utils import session
        from hvac.engine import events
        session.manager = session.SessionManager(events.EventBus())