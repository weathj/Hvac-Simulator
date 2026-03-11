import datetime
import asyncio
from hvac.models import AirUnit, Zone
from hvac.engine import simulation

manager = None # global manager instance

class Session:
    def __init__(self, id):
        self.id = id
        self.active = False
        self.sim = None

    async def start_session(self):
        self.active = True
        self.last_update = datetime.datetime.now()
        self.sim = simulation.Simulation(self.id)
        await asyncio.to_thread(self.sim.calculate)

    def end_session(self):
        self.active = False
        AirUnit.objects.filter(session_id=self.id).delete()
        Zone.objects.filter(session_id=self.id).delete()
    
class SessionManager:
    def __init__(self, event_bus):
        self.bus = event_bus
        self.active_sessions = {}
        self.saved_sessions = {}

    def generate_id(self):
        return max(self.active_sessions.keys(), default=0) + 1
                
    def new_session(self):
        id = self.generate_id()
        self.active_sessions[id] = Session(id)
        current_session = self.active_sessions[id]
        asyncio.create_task(current_session.start_session())