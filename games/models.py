from django.db import models
from sys import maxsize


# Create your models here.
class RandomManager(models.Manager):
    def get_queryset(self):
		# inefficient for large tables, need to find alternative
        return super(RandomManager, self).get_queryset().order_by('?')

class GameType(models.Model):
    types_list = (
        ('WUR', 'Would You Rather...?'),
        ('TOD', 'Truth or Dare'),
        ('ACT', 'Activity'),
        ('DIS', 'Discuss'),
        ('OTH', 'Other')
    )
    game_type = models.CharField(max_length=3, choices=types_list, default=types_list[0][0])
    num_players = models.IntegerField(default=2)
    min_players = models.IntegerField(default=2)
    max_players = models.IntegerField(default=2)

    def __str__(self):
        return "{}: {} ({} Players)".format(self.game_type,
                                            self.get_game_type_display(),
                                            self.num_players)

class Game(models.Model):
    game_type = models.ForeignKey(GameType, default="",
                             on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    def __str__(self):
        type_str = self.game_type.get_game_type_display()
        return "{}: {}".format(type_str, self.text)
