import datetime
import asyncio
import traceback
import uuid
from enum import Enum
from hvac.models import AirUnit, Zone
from hvac.engine import simulation

manager = None # global manager instance

class SessionStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Session:
    def __init__(self, id):
        self.id = id
        self.active = False
        self.status = SessionStatus.OFFLINE
        self.sim = None

    async def start_session(self):
        try:
            self.active = True
            self.last_update = datetime.datetime.now()
            self.sim = simulation.Simulation(self.id)
            await asyncio.to_thread(self.sim.calculate)
        except Exception as e:
            print(f"Session {self.id} failed: {e}")
            traceback.print_exc()

    def end_session(self):
        self.active = False
        AirUnit.objects.filter(session_id=self.id).delete()
        Zone.objects.filter(session_id=self.id).delete()

    def to_dict(self):
        return {
            "session_id" : str(self.id),
            "session_status" : self.status.value
        }
    
class SessionManager:
    def __init__(self, event_bus):
        self.bus = event_bus
        self.active_sessions = {}
        self.saved_sessions = {}

    def generate_id(self):
        return uuid.uuid4()

    def new_session(self):
        id = self.generate_id()
        self.active_sessions[id] = Session(id)
        current_session = self.active_sessions[id]
        asyncio.create_task(current_session.start_session())
        return current_session
    
    def delete_session(self, session_id):
        self.active_sessions[session_id].sim.cleanup(session_id)
        del self.active_sessions[session_id]