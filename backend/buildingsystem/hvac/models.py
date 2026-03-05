from django.db import models

class Air(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    temp = models.FloatField(default=72)
    humidity = models.FloatField(default=60)
    density = models.FloatField(default=0.075)  # lb/ft^3
    heat_capacity = models.FloatField(default=1.08)  # BTU/lb-F
    cfm = models.FloatField(default=25000)
    specific_heat = models.FloatField(default=0.24)  # BTU/lb-F
    btu = models.FloatField(default=0)  # BTU per minute
    pressure = models.FloatField(default=0.4)  # in WC

class Fan(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    speed = models.FloatField(default=0)  # 0-100 Percentage
    velocity = models.FloatField(default=0) # FPM
    max_velocity = models.FloatField(default=800)  # FPM
    min_velocity = models.FloatField(default=200) # FPM
    fan_sts = models.BooleanField(default=False)

class Damper(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    position = models.FloatField(default=0)  # 0-100 Percentage
    area = models.FloatField(default=25) # ft^2
    height = models.FloatField(default=5)
    width = models.FloatField(default=5)

class Coil(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    height = models.FloatField(default=5)
    width = models.FloatField(default=5)
    temp = models.FloatField(default=70)

class AirUnit(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    sa_temp = models.FloatField(default = 55) # °F
    sa_humidity = models.FloatField(default = 40) # %Rh
    sa_btu = models.FloatField(default = 0) # btu/hr
    sa_fan_speed = models.FloatField(default = 100) # Speed %
    sa_flow = models.FloatField(default=38000) # CFM
    cooling_coil_temp = models.FloatField(default=70) # °F
    heating_coil_temp = models.FloatField(default=70) # °F

    ma_temp = models.FloatField(default = 60) # °F
    ma_humidity = models.FloatField(default = 40) # %Rh

    ra_temp = models.FloatField(default = 72) # °F
    ra_fan_speed = models.FloatField(default = 100) # Speed %
    ra_flow = models.FloatField(default=38000) # CFM
    ma_damper_position = models.FloatField(default = 0) # Position open %
    ea_damper_position = models.FloatField(default = 100) # Position open %

    oa_temp = models.FloatField(default = 80) # °F
    oa_humidity = models.FloatField(default = 40) # %Rh
    oa_btu = models.FloatField(default = 0) # btu/hr
    oa_damper_position = models.FloatField(default = 100) # Position open %
    outdoor_air_flow = models.FloatField(default=42000) # CFM


class Zone(models.Model):
    name = models.CharField(max_length=100, default="Empty")
    air_temp = models.FloatField(default=60) # °F
    setpoint = models.FloatField(default=65) # °F
    vav_sa_temp = models.FloatField(default=60) # °F
    vav_dpr_pos = models.FloatField(default=100) # Position open %
    trend_logs = models.JSONField(default=dict)
    height = models.FloatField(default=10)
    width = models.FloatField(default=10)
    length = models.FloatField(default=10)
    volume = models.FloatField(default=1000)
