from django.core.management.base import BaseCommand
from hvac.models import AirUnit, Zone, Air
from hvac.engine import core as c
from hvac.engine import events
from hvac.engine import trends
from hvac.engine.trends import TrendType
from hvac.utils import dbsaver
import json
import time

class Command(BaseCommand):
    help = "Runs the HVAC Simulation loop"

    def handle(self, *args, **options):
        self.stdout.write('Starting simualtion... ')

        bus = events.EventBus()
        tick = 0

        # Single Air Handler for now
        airunit_db = AirUnit.objects.get(pk=1)
        air_unit = c.AirUnit()

        # Iterating through Zone objects to get two clean dictionaires keyed by id.
        # zones = Class Instances, zones_db = Database objects
        zones = {}
        zones_db   = {}
        for zone in Zone.objects.all():
            zones[zone.id] = c.Zone(zone.name, zone.height, zone.width, zone.length)
            zones[zone.id].startup()
            zones[zone.id].trend_logs["zone_temp"] = trends.TrendLog("air_temp", trends.TrendType.ZONE, bus)
            zones[zone.id].trend_logs["zone_spt"] = trends.TrendLog("setpoint", trends.TrendType.ZONE, bus)
            zones_db[zone.id] = zone
            

        # Dynamically write database changes to keep sim loop decoupled from logic
        db = dbsaver.DBSaver(zones_db, airunit_db)
        bus.subscribe('state_updated', db.update_data)

        air_unit.startup()

        self.stdout.write('Air handler online...')

        print(air_unit.unit_sts)

        while air_unit.unit_sts:
            # Pulling write values back from database before heat_cool to catch any changes from frontend.
            for zone_id, zone_obj in zones.items():
                zones_db[zone_id].refresh_from_db()
                zone_obj.vav.damper.position = zones_db[zone_id].vav_dpr_pos
                zone_obj.setpoint = zones_db[zone_id].setpoint

            zone_states, airunit_state = air_unit.heat_cool(zones)
            bus.publish('state_updated', [zone_states, airunit_state])
            bus.publish('time', tick)
            tick += 1
            time.sleep(0.5)