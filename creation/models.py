from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return "{}".format(self.title)

class User(models.Model):
    name = models.CharField(max_length=255)

class Event(models.Model):
    title = models.CharField(max_length=255)
    #admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="event_admin")
    admin = models.CharField(max_length=100);
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="event_user")
    created_date = models.DateTimeField(
            default=timezone.now) 

# Create your models here.
