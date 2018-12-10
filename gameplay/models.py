from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from creation.models import Event, EventUser, Group, Grouping
from games.models import Game
from .utils import max_groups, _random_grps
import random
import sys

class GameManager(models.Model):
    event = models.OneToOneField(Event, default="", on_delete=models.CASCADE)
    round_num = models.IntegerField(default=0)
    max_groups = models.IntegerField(default=100)

    def __str__(self):
        return str(self.pk) + " " + repr(self.event)

    def players(self):
        """Players that have this instance of SimulatedAnnealing as game_org"""
        return {player.user.pk for player in self.player_set.all()}

    def remove_player(self, player):
        try:
            player = Player.objects.get(pk=player) if isinstance(
                player, int) else player
            if player.user.pk in self.players():
                player.delete()
                setattr(player.user, 'player', None)
                self.max_groups = max_groups(self.player_set.count())
                self.save()
        except ObjectDoesNotExist:
            pk = player if isinstance(player, int) else player.pk
            error = "Error: Player {} does not exist. Maybe you gave the \
                     EventUser ID?"
            print(error.format(pk)) # ok if doesn't exist, swallow exception


    def add_player(self, eventuser):
        try:
            user = (EventUser.objects.get(user=eventuser)
                        if isinstance(eventuser, int) else eventuser)

            if not isinstance(user, EventUser):
                user = user.filter(events__access_code = self.event.access_code)[0]
            if user in self.event.users() and not user.is_playing():
                if user.pk in self.players():
                    return #already added
                player = Player(user=user, game_manager=self)
                player.save()
                self.player_set.add(player)
                self.max_groups = max_groups(self.player_set.count())
                self.save()
            elif user not in self.event.users():
                raise AttributeError(
                    "Player {} is not a user registered for this event".format(user[0].user_id))
            # else:
            #     raise RuntimeError("User is already playing a game")
        except ObjectDoesNotExist:
            pk = user if isinstance(user, int) else user.pk
            error = "Error: EventUser {} does not exist"
            print(error.format(pk))
            raise 

    def sync_users(self):
        """Adds all users in the event to the game"""
        players = self.players()
        if self.event.user_count() != len(players):
            event_users = self.event.users()
            for user in event_users:
                if user.pk not in players:
                    self.add_player(user)
        assert(self.max_groups != 100)

    def go_round(self):
        if self.round_num == 0:
            self.event.is_playing = True
            self.event.save()
        if self._generate():
            self._assign_games()
            return True
        else:
            return False

    def end_game(self):
        self.event.is_playing = False
        players = self.player_set.all()
        for player in players:
            self.remove_player(player)
        self.event.delete_groupings()
        setattr(self.event, 'gamemanager', None)
        self.delete()

    def random_groups(self):
        event_users = self.players()
        groupings_ids = _random_grps(event_users)
        grouping = Grouping(event=self.event, is_current=True)
        grouping.save()
        for group in groupings_ids:  # make group for grouping
            g = Group(grouping=grouping)
            g.save()
            for user_id in group:  # add user to group
                g.eventuser_set.add(EventUser.objects.get(pk=user_id))
        return grouping

    def get_current_grouping(self):
        assert(self.event.grouping_set.filter(is_current=True).count() == 1)
        return self.event.grouping_set.filter(is_current=True)[0]

    def _find_duplicate_groups(self, grouping):
        past_groups = self.event.get_grouping_hist().groups()
        current_groups = grouping.groups()

        duplicate_groups = []
        for group in current_groups:
            if group in past_groups:
                duplicate_groups.append(group)
        return duplicate_groups

    def _generate(self):
        if self.round_num == 0:
            if self.event.has_current_grouping():
                self.event.save_group_history()
            self.round_num = 1
            print(self)
            self.save()
            return self.random_groups()
        if (self.max_groups == sys.maxsize or self.round_num < self.max_groups):
            if self.event.has_current_grouping():
                self.event.save_group_history()
            new_grouping = self.random_groups()
            duplicate_groups = self._find_duplicate_groups(new_grouping)
            while duplicate_groups:
                for g in self.event.grouping_set.filter(is_current=True):
                    g.delete()
                new_grouping = self.random_groups()
                duplicate_groups = self._find_duplicate_groups(new_grouping)
            self.round_num += 1
            self.save()
            return new_grouping
        else:
            return None

    def _assign_games(self):
        grouping = self.get_current_grouping()
        for group in grouping.groups():
            nplayers = group.size()
            filtered_games = Game.objects.nplayer_games(nplayers)
            group.game = random.choice(list(filtered_games))
            group.save()


class Player(models.Model):
    user = models.OneToOneField(EventUser, on_delete=models.CASCADE)
    game_manager = models.ForeignKey(GameManager, on_delete=models.CASCADE)

    def remove_self(self):
        self.game_manager.remove_player(self)

    def __str__(self):
        username = self.user.user.username
        event = self.game_manager.event
        return "Player ID {}: {}".format(self.pk, username)
