from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from creation.models import Event, EventUser, Group, Grouping
from games.models import Game
from .utils import max_groups, _random_grps
import random


class GameManager(models.Model):
    event = models.OneToOneField(Event, default="", on_delete=models.CASCADE)
    round_num = models.IntegerField(default=0)
    max_groups = models.IntegerField(default=100)

    def players(self):
        """Players that have this instance of SimulatedAnnealing as game_org"""
        return {player.user.pk for player in self.player_set.all()}

    def remove_player(self, player):
        try:
            player = Player.objects.get(pk=player) if isinstance(
                player, int) else player
            if player.pk in self.players():
                player.delete()
        except ObjectDoesNotExist:
            pk = player if isinstance(player, int) else player.pk
            error = "Error: Player {} does not exist. Maybe you gave the \
                     EventUser ID?"
            print(error.format(pk)) # ok if doesn't exist, swallow exception


    def add_player(self, eventuser):
        try:
            user = (EventUser.objects.get(pk=eventuser) 
                        if isinstance(eventuser, int) else eventuser)
            if user in self.event.users() and not user.is_playing():
                player = Player(user=user, game_manager=self)
                player.save()
                self.player_set.add(player)
            elif user not in self.event.users():
                raise AttributeError(
                    "Player {} is not a user registered for this event".format(user.pk))
            else:
                raise RuntimeError("User is already playing a game")
        except ObjectDoesNotExist:
            pk = user if isinstance(user, int) else user.pk
            error = "Error: EventUser {} does not exist"
            print(error.format(pk))
            raise # problem if doesn't exist, might be bug, so raise

    def sync_users(self):
        """Adds all users in the event to the game"""
        players = self.players()
        if self.event.user_count() != len(players):
            event_users = self.event.users()
            for user in event_users:
                self.add_player(user)

    def go_round(self):
        if round_num == 0:
            self.event.is_playing = True
        self.max_groups = max_groups(len(self.players()))
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
        assert(self.event.grouping_set.filter(is_current=True).count() <= 1)
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
            self.round_num = 1
            return self.random_groups()
        if (self.max_groups == float('inf') or
                self.round_num < self.max_groups):
            if self.event.has_current_grouping():
                self.event.save_group_history()
            new_grouping = self.random_groups()
            duplicate_groups = self._find_duplicate_groups(new_grouping)
            while duplicate_groups:
                # needs refactoring
                if self.event.has_current_grouping():
                    self.event.save_group_history()
                new_grouping = self.random_groups()
                duplicate_groups = self._find_duplicate_groups(new_grouping)
                if not duplicate_groups:
                    self.round_num += 1
                    return new_grouping
                if len(duplicate_groups) >= 2:
                    group1, group2 = random.sample(duplicate_groups, 2)
                else:
                    group1 = duplicate_groups[0]
                    group2 = random.choice(new_grouping.groups())
                new_grouping.random_swap(group1, group2)
                duplicate_groups = self._find_duplicate_groups(new_grouping)
            self.round_num += 1
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

    def __str__(self):
        username = self.user.user.username
        event = self.game_manager.event
        return "Player ID {}: {}".format(self.pk, username)
