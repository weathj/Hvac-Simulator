"""
Dynamically write database changes to keep sim loop decoupled from logic.
Dictionary keys MUST match Model data fields for this to work.
"""
class DBSaver():
    def __init__(self, zones_db, airunit_db):
        self.zones_db = zones_db
        self.airunit_db = airunit_db
    
    def update_data(self, data):
        zone_states, airunit_state = data

        for key, value in airunit_state.items():
            if hasattr(self.airunit_db, key):
                setattr(self.airunit_db, key, value)
        self.airunit_db.save()

        for zone_id, zone_state in zone_states.items():
            for key, value in zone_state.items():
                if hasattr(self.zones_db[zone_id], key):
                    setattr(self.zones_db[zone_id], key, value)
            self.zones_db[zone_id].save()