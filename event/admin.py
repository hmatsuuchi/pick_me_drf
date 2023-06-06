from django.contrib import admin
from .models import Event, EventData, EventTempate

admin.site.register(Event)
admin.site.register(EventData)
admin.site.register(EventTempate)