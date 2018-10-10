from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255)
    #admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="event_admin")
    admin = models.CharField(max_length=100);
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    # users = models.ManyToManyField(User, related_name="event_user")
    created_date = models.DateTimeField(
            default=timezone.now) 
    access_code = models.CharField(max_length=8)

class Group(models.Model):
	event = models.ForeignKey(Event, )
	
class User(models.Model):
	event = models.ForeignKey(Event, )
    name = models.CharField(max_length=255)

# Create your models here.
