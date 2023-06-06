from django.db import models
from event.models import Event, EventTempate

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class AttendeeData(models.Model):
    atendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event_template = models.ManyToManyField(EventTempate)
    value_character = models.CharField(max_length=256, blank=True, null=True)
    value_datetime = models.DateTimeField(blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Attendee Data'
        verbose_name_plural = verbose_name