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

    @property
    def user_count(self):
        return self.eventuser_set.count()
    
    @property
    def curr_grouping(self):
        groups = self.grouping_set.filter(is_current=True)
        if not groups:
            groups = Grouping(event=self)
            groups.save()
        return groups
    
    def get_grouping_hist(self):
        past_groups = self.grouping_set.filter(is_current=False)
        if not past_groups.exists():
            past_groups = Grouping(event=self, is_current=False)
            past_groups.save()
        elif past_groups.count() > 1:  # merge
            history = Grouping(event=self, is_current=False)
            history.save()
            for grouping in past_groups:
                groups = grouping.groups()
                for group in groups:
                    history.group_set.add(group)
                if not grouping.groups():
                    grouping.delete()
                else:
                    raise RuntimeError("Grouping can't be deleted, not empty")
            return history
        else:
            past_groups = list(past_groups)[0]
        return past_groups
    
    def save_group_history(self):
        curr_groups = self.grouping_set.filter(is_current=True)
        if not curr_groups.exists():
            raise AttributeError("Error: No Groupings to save")
        if curr_groups.count() > 1:
            raise AttributeError("Error: More than one current grouping")
        
        past_groups = self.get_grouping_hist() 
        
        for group in list(curr_groups)[0].groups():
            past_groups.group_set.add(group)

    def users(self):
        return {user for user in self.eventuser_set.all()}

    def __str__(self):
        return "{}: {}".format(self.title, self.description)

# a complete grouping of users in an event
class Grouping(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    is_current = models.BooleanField(default=True)

    def groups(self):
        return [group for group in self.group_set.all()]
    
    def __str__(self):
        return "Grouping {} in '{}' Event".format(self.pk, self.event)

class Group(models.Model):
    # curr_size = models.IntegerField(default=0)
    max_size = models.IntegerField(default=9)
    grouping = models.ForeignKey(Grouping, on_delete=models.DO_NOTHING, null=True)

    @property
    def size(self):
        if self.eventuser_set.exists():
            return self.eventuser_set.count()
        else:
            return 0
    
    def users(self):
        return {user for user in self.eventuser_set.all()}
    
    def __eq__(self, other):
        if self.size != other.size:
            return False
        if isinstance(other, Group):
            return self.users() == other.users()
        return False

    def __str__(self):
        people = 'people' if self.size != 1 else 'person'
        return "[Group {}: {} {}]".format(self.pk, self.size, people)

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    events = models.ManyToManyField(Event, related_name='event_users')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return "{}".format(self.user.username)
    
    def __unicode__(self):
        return self.user
