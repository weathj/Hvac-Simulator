import datetime
import asyncio
from hvac.engine import simulation

manager = None # global manager instance

class Session:
    def __init__(self, id, max_length = 2):
        self.id = id
        self.start_time = 0
        self.current_time = self.start_time
        self.max_datetime = datetime.timedelta(hours = max_length)
        self.session_data_map = {}
        self.end_session = False
        self.sim = None

    async def start_session(self):
        self.start_time = datetime.datetime.now()
        self.sim = simulation.Simulation(self.id)
        await self.sim.calculate()

    def update_session_time(self):
        self.max_length = self.start_time - datetime.datetime.now()
        if self.current_time > self.max_datetime:
            self.end_session = True
    
    def get_session_length(self):
        return self.current_time - datetime.datetime.now()
    
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
        
    