from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Group(models.Model):
    pass

class Blog(models.Model):
    title = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return "{}".format(self.title)

class Event(models.Model):
    title = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now)
    access_code = models.CharField(max_length=8)

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)



# Create your models here.



