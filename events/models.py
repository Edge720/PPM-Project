import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField('Event date')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    event_desc = models.CharField(max_length=400,null=True)
    def __str__(self):
        return self.event_name
