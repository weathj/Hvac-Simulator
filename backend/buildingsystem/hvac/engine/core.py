from enum import Enum

class AirUnitState(Enum):
    SHUTDOWN = "shutdown"
    STARTUP = "startup"
    HEATING = "heating"
    COOLING = "cooling"

class Air:
    def __init__(self, time_step=60):
        self.temp = 60.0
        self.humidity = 40.0
        self.density = 0.075  # lb/ft^3
        self.heat_capacity = 1.08  # BTU/lb-F
        self.cfm = 0.0
        self.specific_heat = 0.24  # BTU/lb-F
        self.btu = 0.0  # BTU per minute
        self.pressure = 0.4  # in WC
        self.time_step = 60  # seconds

    def calculate_btu(self, target_temp):
        max_temp_change = abs(target_temp - self.temp)
        mass_flow = self.cfm * self.density

        # Limit the temperature change based on a realistic rate
        # Assume a maximum temperature change rate of 5°F per minute
        max_rate = 5 * (self.time_step / 60)  # °F per time_step
        actual_temp_change = min(max_temp_change, max_rate)

        # Maintain the sign of the original temperature difference
        if target_temp < self.temp:
            actual_temp_change = -actual_temp_change

        # Calculate BTU per hour
        btu_per_hour = mass_flow * self.specific_heat * actual_temp_change

        # Convert to BTU per time_step
        btu = btu_per_hour * (self.time_step / 3600)

        self.btu = btu

        return btu
    
    def update_temp(self, btu):
        # Update the temperature based on the BTU transfer
        if self.cfm == 0:
            return 
        temp_change = btu / (self.density * self.cfm * self.specific_heat * (self.time_step / 60))
        self.temp += temp_change
    
    def set_btu(self, btu):
        self.btu = btu
        return self.btu
    
    def get_temp(self):
        return self.temp
    
    def set_temp(self, temp):
        self.temp = temp
        return self.temp

    def calculate_pressure(self, pressure, incoming_cfm, volume):
        # Future implementation - pressure differential tracking
        # Currently not wired into simulation loop
        cfm_offset = abs(self.cfm - incoming_cfm)
        air_change_rate = (cfm_offset * (self.time_step / 3600)) / volume  # ACH due to offset
        volume_change = (volume * air_change_rate) * self.time_step / 60  # Volume change in one minute
        new_volume = volume + volume_change
        p2 = pressure * (volume / new_volume)
        return p2 - pressure

    
class OutdoorAir(Air):
    def __init__(self):
        super().__init__()
        self.temp = 80.0
        self.humidity = 40.0
        self.density = 0.075  # lb/ft^3
        self.heat_capacity = 1.08  # BTU/lb-F
        self.cfm = 8000.0
        self.specific_heat = 0.24  # BTU/lb-F
        self.btu = 0.0  # BTU per minute
        self.pressure = 0.4  # in WC
        self.time_step = 60  # seconds

class VAV:
    def __init__(self):
        self.damper = Damper()
        self.fan = None
        self.sa = Air()
        self.heating_coil = None



class Zone:
    def __init__(self, session_id, name, height = 10, width = 10, length = 10):
        self.session_id = session_id
        self.name = name
        self.air = Air()
        self.vav = VAV()
        self.setpoint = 0
        self.height = height
        self.width = width
        self.length = length
        self.volume = self.calculate_volume()
        self.trend_logs = {}

    def startup(self):
        # VAV needs to be calculated prior to zones as the air is moving through it.
        self.vav.damper.set_position(100)

    def calculate_volume(self):
        return self.height * self.width * self.length

    def set_temp(self, temp, ahu_runtime):
        new_temp = self.air.temp + temp
        self.air.temp = new_temp

class Fan:
    def __init__(self, max_cfm=2000, min_cfm=200,  time_step=60):
        self.speed = 0.0  # 0-100 Percentage
        self.cfm = 0.0
        self.max_cfm = max_cfm
        self.physical_max_cfm = max_cfm
        self.min_cfm = min_cfm
        self.min_speed = 20 #%
        self.fan_sts = False
        self.time_step = time_step
        self.area = 100 # ft^2

    def set_speed(self, speed):
        self.speed = max(0, min(100, speed))
        self.cfm = self.min_cfm + (self.speed / 100) * (self.max_cfm - self.min_cfm)
        return self.cfm * (self.time_step / 60)  # Return CFM for the given time step
    
    def set_incoming_cfm(self, incoming_cfm):
        self.max_cfm = min(incoming_cfm, self.physical_max_cfm)

    def startup(self):
        self.fan_sts = True
        self.set_speed(self.min_speed)
        return self.fan_sts

    def shutdown(self):
        self.fan_sts = False
        return self.fan_sts
    
    def get_cfm(self):
        return self.cfm

    def get_velocity(self):
        return self.cfm / self.area


class Damper:
    def __init__(self, time_step=60):
        self.position = 0.0  # 0-100 Percentage
        self.time_step = time_step

    def open(self):
        self.position = 100

    def close(self):
        self.position = 0

    def set_position(self, position):
        self.position = max(0, min(100, position))

    def get_position(self):
        return self.position

    def get_cfm(self, incoming_cfm):
        return incoming_cfm * (self.position / 100) * (self.time_step / 60)

class Coil:
    def __init__(self, height=5, width=5, time_step=60):
        self.height = height
        self.width = width
        self.temp = 0.0
        self.time_step = time_step

    def get_area(self):
        return self.height * self.width
    
    def get_temp(self):
        return self.temp
    
    def update_temp(self, air):
        # Estimate temperature of coil based on air moving across
        temp_change = air.btu / (air.density * air.heat_capacity * air.specific_heat)
        self.temp += temp_change


class AirUnit:
    def __init__(self, session_id, oa= None, sa=None, ma=None, ra=None, supply_fan=None, return_fan=None,
                 ra_damper=None, ea_damper=None, oa_damper=None, cooling_coil=None, heating_coil=None, time_factor=1):
        self.session_id = session_id
        self.unit_sts = False
        self.state = AirUnitState.SHUTDOWN

        self.sa = sa if sa is not None else Air()
        self.supply_fan = supply_fan if supply_fan is not None else Fan(40000, 8000)
        self.supply_air_flow = None
        self.cooling_coil = cooling_coil if cooling_coil is not None else Coil(5, 5)
        self.heating_coil = heating_coil if heating_coil is not None else Coil(5, 5)

        self.ma = ma if ma is not None else Air()

        self.ra = ra if ra is not None else Air()
        self.return_air_flow = None
        self.return_fan = return_fan if return_fan is not None else Fan(40000, 8000)
        self.ra_damper = ra_damper if ra_damper is not None else Damper()
        self.ea_damper = ea_damper if ea_damper is not None else Damper()

        self.oa = oa if oa is not None else OutdoorAir()
        self.oa_damper = oa_damper if oa_damper is not None else Damper()
        self.outdoor_air_flow = None

        self.supply_air_flow = 0.0
        self.return_air_flow = 0.0
        self.outdoor_air_flow = 0.0

        self.ahu_runtime = 0.0
        self.time_factor = time_factor

    def startup(self):
        self.unit_sts = True
        self.state = AirUnitState.STARTUP

        # Set air moving to allow Air Handler to turn on
        self.supply_fan.startup()
        self.return_fan.startup()

        self.cooling_coil.temp = 65
        self.heating_coil.temp = 65

        self.ra_damper.set_position(20)

        self.oa_damper.set_position(80)
        self.ea_damper.set_position(80)

        self.state = AirUnitState.COOLING if self.oa.temp > 80 else AirUnitState.HEATING

        return self.unit_sts

    def shutdown(self):
        self.unit_sts = False
        self.state = AirUnitState.SHUTDOWN
        return self.unit_sts

    # This is the key function, this is the air moving through the unit.
    def heat_cool(self, zones):
        if not self.unit_sts or self.state == AirUnitState.SHUTDOWN:
            return self.__dict__()

        # Calculate air flows
        # Dampers determine max available flow using fan physical capacity
        oa_max = self.oa_damper.get_cfm(self.supply_fan.physical_max_cfm)
        ra_available = self.return_fan.physical_max_cfm * (1 - self.ea_damper.position / 100)
        ra_max = self.ra_damper.get_cfm(ra_available)

        # Fan effective range is limited by what dampers allow
        self.supply_fan.set_incoming_cfm(oa_max + ra_max)
        self.return_fan.set_incoming_cfm(ra_max)

        # Fan speed determines actual CFM within that range
        self.supply_fan.set_speed(self.supply_fan.speed)
        self.return_fan.set_speed(self.return_fan.speed)

        supply_cfm = self.supply_fan.get_cfm()
        return_cfm = self.return_fan.get_cfm()
        self.supply_air_flow = supply_cfm
        self.return_air_flow = return_cfm

        # Distribute actual CFM proportionally through OA/RA
        ma_max = oa_max + ra_max
        self.oa.cfm = supply_cfm * (oa_max / ma_max) if ma_max else 0
        self.ra.cfm = supply_cfm - self.oa.cfm
        self.outdoor_air_flow = self.oa.cfm
        self.ma.cfm = self.oa.cfm + self.ra.cfm
        self.sa.cfm = self.ma.cfm

        # Check for airflow as we would in real life
        if self.supply_fan.cfm == 0 or self.return_fan.cfm == 0:
            return self.__dict__()
        
        if self.ma.cfm == 0:
            return self.__dict__()
        
        self.ma.temp = (self.oa.temp * self.oa.cfm + self.ra.temp * self.ra.cfm) / self.ma.cfm

        cooling_btu, heating_btu = 0

        # Calculate cooling and heating effects
        if self.state == AirUnitState.COOLING:
            cooling_btu = self.ma.calculate_btu(self.cooling_coil.temp)
            self.sa.update_temp(cooling_btu)
            self.heating_coil.update_temp(self.ma.air)

        if self.state == AirUnitState.HEATING:
            heating_btu = self.ma.calculate_btu(self.heating_coil.temp)
            self.sa.update_temp(heating_btu)
            self.cooling_coil.update_temp(self.sa.air) # Need to apply already heated air since cooling coil is past the heating coil

        net_btu = cooling_btu + heating_btu
        self.sa.btu = net_btu

        zone_temps  = []
        zone_states = {}

        for zone_id, zone_object in zones.items():
            zone_object.vav.sa.cfm = zone_object.vav.damper.get_cfm(self.supply_air_flow)
            zone_object.vav.sa.temp = self.sa.temp

            if zone_object.vav.heating_coil:
                vav_reheat_btu = zone_object.vav.sa.calculate_btu(zone_object.vav.heating_coil.temp)
                zone_object.vav.sa.update_temp(vav_reheat_btu)

            zone_object.air.cfm = zone_object.vav.sa.cfm

            zone_btu = zone_object.air.calculate_btu(zone_object.vav.sa.temp)

            zone_object.air.update_temp(zone_btu / (zone_object.air.density * zone_object.air.specific_heat * 1000))
            zone_temps.append(zone_object.air.temp)
        

            zone_states[zone_id] = {
                "air_temp": zone_object.air.temp,
                "setpoint": zone_object.setpoint,
                "vav_sa_temp" : zone_object.vav.sa.temp,
                "vav_dpr_pos" : zone_object.vav.damper.position,
                "height" : zone_object.height,
                "width" : zone_object.width,
                "length" : zone_object.length,
                "volume" : zone_object.volume,
                "trend_logs" : {k: v.Save() for k, v in zone_object.trend_logs.items()}
            }
        
        
        self.ra.temp = sum(zone_temps) / len(zone_temps)

        
        airunit_state = {
            "sa_temp": self.sa.temp,
            "sa_humidity": self.sa.humidity,
            "sa_btu": self.sa.btu,
            "sa_fan_speed": self.supply_fan.speed,
            "sa_flow": self.supply_air_flow,
            "cooling_coil_temp": self.cooling_coil.temp,
            "heating_coil_temp": self.heating_coil.temp,
            "ma_temp": self.ma.temp,
            "ma_humidity": self.ma.humidity,
            "ma_btu": self.ma.btu,
            "ma_flow": self.ma.cfm,
            "ra_temp": self.ra.temp,
            "ra_fan_speed": self.return_fan.speed,
            "ra_flow": self.return_air_flow,
            "ra_damper_position": self.ra_damper.position,
            "ea_damper_position": self.ea_damper.position,
            "oa_temp": self.oa.temp,
            "oa_humidity": self.oa.humidity,
            "oa_btu": self.oa.btu,
            "oa_damper_position": self.oa_damper.position,
            "outdoor_air_flow": self.outdoor_air_flow,
        }

        return zone_states, airunit_state
    
    def __dict__(self):
        return {
            "sa_temp": self.sa.temp,
            "sa_humidity": self.sa.humidity,
            "sa_btu": self.sa.btu,
            "sa_fan_speed": self.supply_fan.speed,
            "sa_flow": self.supply_air_flow,
            "cooling_coil_temp": self.cooling_coil.temp,
            "heating_coil_temp": self.heating_coil.temp,
            "ma_temp": self.ma.temp,
            "ma_humidity": self.ma.humidity,
            "ma_btu": self.ma.btu,
            "ra_temp": self.ra.temp,
            "ra_fan_speed": self.return_fan.speed,
            "ra_flow": self.return_air_flow,
            "ra_damper_position": self.ra_damper.position,
            "ea_damper_position": self.ea_damper.position,
            "oa_temp": self.oa.temp,
            "oa_humidity": self.oa.humidity,
            "oa_btu": self.oa.btu,
            "oa_damper_position": self.oa_damper.position,
            "outdoor_air_flow": self.outdoor_air_flow,
        }
