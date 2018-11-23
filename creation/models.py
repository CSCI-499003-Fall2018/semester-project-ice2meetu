from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from games.models import Game, GameType#, SimulatedAnnealing
import random

class Event(models.Model):
    title = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(default="", max_length=500)
    event_type = models.CharField(max_length=100)
    created_date = models.DateTimeField(
        default=timezone.now)
    access_code = models.CharField(max_length=8)
    is_playing = models.BooleanField(default=False)

    def user_count(self):
        if self.event_users.exists():
            return self.event_users.count()
        else:
            return 0
    
    def has_current_grouping(self):
        return self.grouping_set.filter(is_current=True).exists()
    
    def get_grouping_hist(self):
        past_groups = self.grouping_set.filter(is_current=False)
        if not past_groups.exists():
            past_groups = Grouping(event=self, is_current=False)
            past_groups.save()
        elif past_groups.count() > 1:  # merge
            raise RuntimeWarning("Warning: You have more than one past grouping")
            history = Grouping(event=self, is_current=False)
            history.save()
            for grouping in past_groups:
                groups = grouping.groups()
                for group in groups:
                    history.group_set.add(group)
                grouping.delete()
            return history
        else:
            past_groups = list(past_groups)[0]
        return past_groups
    
    def save_group_history(self):
        curr_groups = self.grouping_set.filter(is_current=True)
        if not curr_groups.exists():
            raise RuntimeError("Error: No Groupings to save")

        past_groups = self.get_grouping_hist() 
        for group in list(curr_groups)[0].groups():
            past_groups.group_set.add(group)
        curr_groups.delete()

        assert(self.grouping_set.filter(is_current=True).count() <= 1)
        assert(self.grouping_set.filter(is_current=False).count() == 1)

    def users(self):
        return {user for user in self.event_users.all()}

    def __str__(self):
        return "{}: {}".format(self.title, self.description)


class Grouping(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    is_current = models.BooleanField(default=True)

    def size(self):
        return self.group_set.count()

    def groups(self):
        return [group for group in self.group_set.all()]
    
    def random_swap(self, group1, group2):
        assert(group1 in self.groups())
        assert(group2 in self.groups())

        player1 = random.choice(list(group1.eventuser_set.all()))
        player2 = random.choice(list(group2.eventuser_set.all()))
        group1.eventuser_set.remove(player1)
        group2.eventuser_set.remove(player2)
        group1.eventuser_set.add(player2)
        group2.eventuser_set.add(player1)
    
    def __str__(self):
        return "Grouping {} in '{}' Event".format(self.pk, self.event)

class Group(models.Model):
    max_size = models.IntegerField(default=9)
    grouping = models.ForeignKey(Grouping, on_delete=models.CASCADE, null=True)
    is_complete = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=True, blank=True)

    @property
    def is_playing(self):
        return self.event().is_playing

    def size(self):
        if self.eventuser_set.exists():
            return self.eventuser_set.count()
        else:
            return 0
    
    def users(self):
        return {user for user in self.eventuser_set.all()}
    
    def event(self):
        return grouping.event
    
    def __eq__(self, other):
        if self.size() != other.size():
            return False
        if isinstance(other, Group):
            return self.users() == other.users()
        return False

    def size(self):
        if self.eventuser_set.exists():
            return self.eventuser_set.count()
        else:
            return 0
    
    def users(self):
        return {user for user in self.eventuser_set.all()}
    
    def event(self):
        return grouping.event
    
    def __eq__(self, other):
        if self.size() != other.size():
            return False
        if isinstance(other, Group):
            return self.users() == other.users()
        return False

    def __str__(self):
        people = 'people' if self.size() != 1 else 'person'
        return "[Group {}: {} {}]".format(self.pk, self.size(), people)

class EventUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, related_name='event_users', blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def is_playing(self):
        return hasattr(self, 'player')
    
    def current_game(self):
        event = self.events.filter(is_playing=True)[0]
        groupings = event.grouping_set.filter(is_current=True)[0]
        group = None
        for g in groupings.groups():
            if g in self.groups.all():
                group = g
        return group.game

    def __str__(self):
        return "{}".format(self.user.username)
    
    def __unicode__(self):
        return self.user
