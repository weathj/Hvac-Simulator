from django.core.management.base import BaseCommand
from hvac.models import AirUnit, Zone, Air
from hvac.engine import core as c
from hvac.engine import events
from hvac.engine import trends
from hvac.engine.trends import TrendType
from hvac.utils import dbsaver
from hvac.utils import session
import json
import time

class Command(BaseCommand):
    help = "Runs the HVAC Simulation loop"

    def handle(self, *args, **options):
        self.stdout.write('Starting simualtion engine... ')

        manager_bus = events.EventBus()
        manager = session.SessionManager(manager_bus)

        while True:
            manager.manage_sessions()

        