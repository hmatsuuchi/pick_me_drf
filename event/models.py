from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class EventData(models.Model):
    class TypeChoices(models.IntegerChoices):
        event_name                      = 1
        event_start_date                = 2
        event_end_date                  = 3
        event_application_start_date    = 4
        event_application_end_date      = 5

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TypeChoices.choices)
    value_character = models.CharField(max_length=256, blank=True, null=True)
    value_datetime = models.DateTimeField(blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Event Data'
        verbose_name_plural = verbose_name

class EventTempate(models.Model):
    name = models.CharField(max_length=256)
    event = models.ManyToManyField(Event)
