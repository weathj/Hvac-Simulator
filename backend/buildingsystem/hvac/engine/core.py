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

        print(f"Temp Change: {actual_temp_change:.2f}°F")
        print(f"BTU: {btu:.2f}")

        self.btu = btu

        return btu
    
    def update_temp(self, btu):
        # Update the temperature based on the BTU transfer
        if self.cfm == 0:
            return 
        temp_change = btu / (self.density * self.cfm * self.specific_heat * (self.time_step / 60))
        self.temp += temp_change
        print(f"New Temp: {self.temp:.2f}°F")
    
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
        self.heating_coil = Coil()



class Zone:
    def __init__(self, name, height, width, length):
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
        self.min_cfm = min_cfm
        self.min_speed = 20 #%
        self.fan_sts = False
        self.time_step = time_step
        self.area = 100 # ft^2

    def set_speed(self, speed):
        self.speed = max(0, min(100, speed))
        self.cfm = self.min_cfm + (self.speed / 100) * (self.max_cfm - self.min_cfm)
        return self.cfm * (self.time_step / 60)  # Return CFM for the given time step

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


class AirUnit:
    def __init__(self, oa= None, sa=None, ma=None, ra=None, supply_fan=None, return_fan=None,
                 ma_damper=None, ea_damper=None, oa_damper=None,
                 cooling_coil=None, heating_coil=None, time_factor=1):
        self.unit_sts = False

        self.sa = sa if sa is not None else Air()
        self.supply_fan = supply_fan if supply_fan is not None else Fan(200, 800)
        self.supply_air_flow = None
        self.cooling_coil = cooling_coil if cooling_coil is not None else Coil(5, 5)
        self.heating_coil = heating_coil if heating_coil is not None else Coil(5, 5)

        self.ma = ma if ma is not None else Air()

        self.ra = ra if ra is not None else Air()
        self.return_air_flow = None
        self.return_fan = return_fan if return_fan is not None else Fan(200, 10000)
        self.ma_damper = ma_damper if ma_damper is not None else Damper()
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

        # Set air moving to allow Air Handler to turn on
        self.supply_fan.startup()
        self.return_fan.startup()

        self.ma_damper.set_position(20)

        self.oa_damper.set_position(80)
        self.ea_damper.set_position(80)

        return self.unit_sts

    def shutdown(self):
        self.unit_sts = False
        return self.unit_sts

    # This is the key function, this is the air moving through the unit.
    def heat_cool(self, zones):
        if not self.unit_sts:
            return self.__dict__()

        # Calculate air flows
        self.supply_fan.set_speed(self.supply_fan.speed)
        self.return_fan.set_speed(self.return_fan.speed)
        
        supply_cfm = self.supply_fan.get_cfm()
        print("Supply CFM:", supply_cfm)
        self.supply_air_flow = supply_cfm
        return_cfm = self.return_fan.get_cfm()
        print("Return CFM:", return_cfm)
        self.return_air_flow = return_cfm
        
        self.oa.cfm = self.oa_damper.get_cfm(supply_cfm)
        self.outdoor_air_flow = self.oa.cfm
        print("Calculated OA CFM:", self.oa.cfm)
        self.ra.cfm = self.ma_damper.get_cfm(return_cfm)
        print("Calculated RA CFM:", self.ra.cfm)
        self.ma.cfm = self.oa.cfm + self.ra.cfm
        print("Calculated MA CFM:", self.ma.cfm)
        self.sa.cfm = self.ma.cfm
        print("Calculated SA CFM:", self.sa.cfm)

        # Check for airflow as we would in real life
        if self.supply_fan.cfm == 0 or self.return_fan.cfm == 0:
            return self.__dict__()
        
        if self.ma.cfm == 0:
            return self.__dict__()
        
        self.ma.temp = (self.oa.temp * self.oa.cfm + self.ra.temp * self.ra.cfm) / self.ma.cfm
        print("Mixed Air Temp:", self.ma.temp)

        # Calculate cooling and heating effects
        cooling_btu = self.ma.calculate_btu(self.cooling_coil.temp)
        self.ma.update_temp(cooling_btu)
        print("Cooling BTU:", cooling_btu)
        heating_btu = self.ma.calculate_btu(self.heating_coil.temp)
        self.ma.update_temp(heating_btu)
        print("Heating BTU:", heating_btu)
        
        net_btu = cooling_btu + heating_btu
        print("Net BTU:", net_btu)
        
        self.sa.temp = self.ma.temp + (net_btu / (self.sa.cfm * self.sa.density * self.sa.specific_heat))
        print("Supply Air Temp:", self.sa.temp)

        zone_temps  = []
        zone_states = {}

        for zone_id, zone_object in zones.items():
            zone_object.vav.sa.cfm = zone_object.vav.damper.get_cfm(self.supply_air_flow)

            if zone_object.vav.heating_coil:
                vav_reheat_btu = zone_object.vav.sa.calculate_btu(zone_object.vav.heating_coil.temp)
                zone_object.vav.sa.update_temp(vav_reheat_btu)

            print("Zone VAV CFM:", zone_object.vav.sa.cfm)
            zone_object.vav.sa.update_temp(self.sa.btu)

            zone_object.air.cfm = zone_object.vav.sa.cfm

            zone_btu = zone_object.air.calculate_btu(zone_object.vav.sa.temp)
            print("Zone BTU:", zone_btu)

            zone_object.air.update_temp(zone_btu / (zone_object.air.density * zone_object.air.specific_heat * 1000))
            print("Zone Temp:", zone_object.air.temp)
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
            "ra_temp": self.ra.temp,
            "ra_fan_speed": self.return_fan.speed,
            "ra_flow": self.return_air_flow,
            "ma_damper_position": self.ma_damper.position,
            "ea_damper_position": self.ea_damper.position,
            "oa_temp": self.oa.temp,
            "oa_humidity": self.oa.humidity,
            "oa_btu": self.oa.btu,
            "oa_damper_position": self.oa_damper.position,
            "outdoor_air_flow": self.outdoor_air_flow,
        }

        self.ra.temp = sum(zone_temps) / len(zone_temps)

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
            "ma_damper_position": self.ma_damper.position,
            "ea_damper_position": self.ea_damper.position,
            "oa_temp": self.oa.temp,
            "oa_humidity": self.oa.humidity,
            "oa_btu": self.oa.btu,
            "oa_damper_position": self.oa_damper.position,
            "outdoor_air_flow": self.outdoor_air_flow,
        }


class Building:
    def __init__(self, ahu):
        self.occupied = False
        self.zones = []
        self.oa = Air()
        self.ahu = ahu

    def add_zone(self, zone):
        self.zones.append(zone)

    def set_occupied(self, occupied):
        self.occupied = occupied

    def set_unoccupied(self):
        self.occupied = False

    def set_ahu(self, ahu):
        self.ahu = ahu

    def get_temp(self, air):
        return air.temp

    def set_temp(self, air, temp):
        air.temp = temp

    def get_damper_position(self, damper):
        return damper.get_position()

    def set_damper_position(self, damper, position):
        damper.set_position(position)

    def get_fan_speed(self, fan):
        return fan.get_speed()

    def set_fan_speed(self, fan, speed):
        fan.set_speed(speed)

    def get_coil_temp(self, coil):
        return coil.temp

    def set_coil_temp(self, coil, temp):
        coil.temp = temp