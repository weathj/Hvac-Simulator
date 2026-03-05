from rest_framework import serializers
from .models import AirUnit, Zone, Air, Damper, Coil, Fan

class AirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Air
        fields = '__all__'

class DamperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Damper
        fields = '__all__'

class CoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coil
        fields = '__all__'

class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class AirUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirUnit
        fields = '__all__'
