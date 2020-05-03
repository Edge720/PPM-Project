import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField('Event date')
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_desc = models.CharField(max_length=400)
    event_reviewed = models.BooleanField(default = False)
    event_location = models.CharField(default = "",max_length=200)
    event_user = models.ForeignKey(User, default=None, on_delete = models.CASCADE)
    def __str__(self):
        return self.event_name

class Review(models.Model):
    event_reviewed = models.ForeignKey(Event, default = None, on_delete = models.CASCADE)
    review = models.CharField(max_length=400)
    attended = models.BooleanField(default = True)
    attendance = models.IntegerField()
    rating = models.IntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    hex_code = models.CharField(max_length=6, default = '#ADD8E6')


    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
