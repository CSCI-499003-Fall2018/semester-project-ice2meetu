from django.db import models
import random

class GameType(models.Model):
    types_list = (
        ('WUR', 'Would You Rather...?'),
        ('TOD', 'Truth or Dare'),
        ('ACT', 'Activity'),
        ('DIS', 'Discuss'),
        ('OTH', 'Other')
    )
    game_type = models.CharField(max_length=3, choices=types_list)
    min_players = models.IntegerField(default=2)
    max_players = models.IntegerField(default=2)

    def __str__(self):
        return "{}: {} ({}-{} Players)".format(self.game_type,
                                            self.get_game_type_display(),
                                            self.min_players, self.max_players)

class GameManager(models.Manager):
    def nplayer_games(self, num_players):
        min_games = Game.objects.filter(
            game_type__min_players__lte=num_players)
        filtered_games = Game.objects.filter(
            game_type__max_players__gte=num_players)
        return filtered_games

class Game(models.Model):
    game_type = models.ForeignKey(GameType, default="",
                             on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True)
    objects = GameManager()

    def get_nplayer_games(nplayers):
        min_games = Game.objects.filter(game_type__min_players__gte=nplayers)
        filtered_games = Game.objects.filter(game_type__max_players__lte=nplayers)
        return list(filtered_games)

    def __str__(self):
        type_str = self.game_type.get_game_type_display()
        return "{}: {}".format(type_str, self.text)



