from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from games.models import Game, GameType

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

class Grouping(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return "Grouping {} in '{}' Event".format(self.pk, self.event)

class Group(models.Model):
    # curr_size = models.IntegerField(default=0)
    max_size = models.IntegerField(default=9)
    grouping = models.ForeignKey(Grouping, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        grp_size = self.eventuser_set.count()
        event = self.grouping.event
        return "[Group {}: {} people]".format(self.pk, grp_size)

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    events = models.ManyToManyField(Event, related_name='event_users')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return "{}".format(self.user.username)
    
    def __unicode__(self):
        return self.user
