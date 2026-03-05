from django.contrib import admin
from .models import AirUnit, Zone, Coil, Fan, Damper, Air

admin.site.register(AirUnit)
admin.site.register(Zone)
admin.site.register(Coil)
admin.site.register(Fan)
admin.site.register(Air)
admin.site.register(Damper)