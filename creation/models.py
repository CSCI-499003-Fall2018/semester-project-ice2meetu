from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now)
    access_code = models.CharField(max_length=8)

    def __str__(self):
        return "{}: {} ".format(self.title, self.description)

class Group(models.Model):
    event = models.ForeignKey(Event, on_delete = models.DO_NOTHING)
    curr_size = models.IntegerField(default=0)
    max_size = models.IntegerField(default=4)
class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='event_users')

    def __unicode__(self):
        return self.user



# Create your models here.





