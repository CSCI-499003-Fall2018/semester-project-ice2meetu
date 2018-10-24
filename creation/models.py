from django.db import models
from django.utils import timezone
from django.contrib.auth import User

class Blog(models.Model):
    title = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return "{}".format(self.title)


class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
class Event(models.Model):
    title = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.CharField(max_length=100);
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    users = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
            default=timezone.now) 
    access_code = models.CharField(max_length=8)

# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(EventUser, on_delete=models.DO_NOTHING)


