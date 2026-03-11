from hvac.models import AirUnit, Zone, Air
from hvac.engine import core as c
from hvac.engine import events
from hvac.engine import trends
from hvac.engine.trends import TrendType
from hvac.utils import dbsaver
import datetime
import json
import time

class Simulation:
    def __init__(self, session_id, zones = 3):
        self.session_id = session_id
        self.zones = zones

    def calculate(self):
        bus = events.EventBus()
        tick = 0

        # Create Air Handler Objects
        airunit_db = AirUnit.objects.create(
            session_id = self.session_id
        )
        air_unit = c.AirUnit()

        # Iterating through Zone objects to get two clean dictionaires keyed by id.
        # zones = Class Instances, zones_db = Database objects
        zones = {}
        zones_db   = {}   

        for zone in range(self.zones):
            zone_obj = c.Zone(self.session_id, f'Zone-{zone}')
            zones[zone] = zone_obj
            zones_db[zone] = Zone.objects.create(
                session_id = self.session_id,
                name = f'Zone-{zone}',
                height = zone_obj.height,
                width = zone_obj.width,
                length = zone_obj.length
            )

            zones[zone].startup()
            zones[zone].trend_logs["zone_temp"] = trends.TrendLog("air_temp", trends.TrendType.ZONE, bus)
            zones[zone].trend_logs["zone_sa_temp"] = trends.TrendLog("vav_sa_temp", trends.TrendType.ZONE, bus)

        # Dynamically write database changes to keep sim loop decoupled from logic
        db = dbsaver.DBSaver(zones_db, airunit_db)
        bus.subscribe('state_updated', db.update_data)

        air_unit.startup()

        # Write startup state to DB so the loop's refresh_from_db reads back the correct values
        airunit_db.cooling_coil_temp  = air_unit.cooling_coil.temp
        airunit_db.heating_coil_temp  = air_unit.heating_coil.temp
        airunit_db.sa_fan_speed       = air_unit.supply_fan.speed
        airunit_db.ra_fan_speed       = air_unit.return_fan.speed
        airunit_db.ra_damper_position = air_unit.ra_damper.position
        airunit_db.ea_damper_position = air_unit.ea_damper.position
        airunit_db.oa_damper_position = air_unit.oa_damper.position
        airunit_db.save()

        if(air_unit.unit_sts):
            print(f'Session: {self.session_id} Air handler online...')
        else:
            print(f'Session: {self.session_id} Air handler failed to start')
            
        while air_unit.unit_sts:
            # Pulling write values back from database before heat_cool to catch any changes from frontend.
            airunit_db.refresh_from_db()
            air_unit.cooling_coil.temp = airunit_db.cooling_coil_temp
            air_unit.heating_coil.temp = airunit_db.heating_coil_temp
            air_unit.supply_fan.speed  = airunit_db.sa_fan_speed
            air_unit.return_fan.speed  = airunit_db.ra_fan_speed
            air_unit.ra_damper.position = airunit_db.ra_damper_position
            air_unit.ea_damper.position = airunit_db.ea_damper_position
            air_unit.oa_damper.position = airunit_db.oa_damper_position
            air_unit.oa.temp           = airunit_db.oa_temp

            for zone_id, zone_obj in zones.items():
                zones_db[zone_id].refresh_from_db()
                zone_obj.vav.damper.position = zones_db[zone_id].vav_dpr_pos
                zone_obj.vav_sa_temp = zones_db[zone_id].vav_sa_temp

            zone_states, airunit_state = air_unit.heat_cool(zones)

            bus.publish('state_updated', [zone_states, airunit_state])
            bus.publish('time', tick)
            tick += 0.5
            time.sleep(0.5)
        