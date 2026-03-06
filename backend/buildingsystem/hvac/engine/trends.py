from enum import Enum

class TrendType(Enum):
    ZONE = "zone"
    AIRUNIT = "airunit"

class TrendLog():
    def __init__(self, point, type :TrendType, event_bus):
        self.point = point
        self.value = None
        self.type = type
        self.interval = 15
        self.intervalsRemaining = self.interval
        self.buffer_size = 50
        self.trend_dict = {}
        self.event_bus = event_bus
        self.event_bus.subscribe("time", self.Trigger)
        self.event_bus.subscribe("state_updated", self.UpdateValue)

    def Save(self):
        return self.trend_dict

    def Log(self, trend_time):
        self.trend_dict[trend_time] = self.value

    def Trigger(self, tick):
        if(self.intervalsRemaining == 0):
            self.Log(tick)
            self.intervalsRemaining = self.interval        
        self.intervalsRemaining -= 1
        self.ManageBuffer()

    def UpdateValue(self, data):
        zone_states, airunit_state = data
        
        if(self.type == TrendType.AIRUNIT):
            if self.point in airunit_state:
                self.value = airunit_state[self.point]

        if(self.type == TrendType.ZONE):
            for zone_id, zone_state in zone_states.items():
                if self.point in zone_state:
                    self.value = zone_state[self.point]

    # Dict should not theoritically be higher than the buffer_size, but incase trends_to_remove should provide an accurate number of trends to remove.
    # This will also be a benefit if the buffer_size can be changed.
    def ManageBuffer(self):
        cache = None # Can make more than 1 trend if needed later

        if len(self.trend_dict) > self.buffer_size:
            trends_to_remove = len(self.trend_dict) - self.buffer_size
            if trends_to_remove > 1:
                for x in range(trends_to_remove - 1):
                    try:
                        cache = self.trend_dict[list(self.trend_dict.keys())[x]] # caching to print information after trend is deleted.
                        del self.trend_dict[list(self.trend_dict.keys())[x]]
                        print(f"Deleted trend due to buffer size: {cache}, Trendlog is now {len(self.trend_dict)} trends long")
                    except(KeyError):
                        print("Unable to delete trend")
                        self.event_bus.publish("failed_trend_delete", cache)

