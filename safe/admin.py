from django.contrib import admin
from .models import SensorType, Sensor, UserExtension
# Register your models here.
admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(UserExtension)
