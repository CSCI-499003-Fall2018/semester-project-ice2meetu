from django.db import models
<<<<<<< HEAD
from sys import maxsize


# Create your models here.
class RandomManager(models.Manager):
    def get_queryset(self):
		# inefficient for large tables, need to find alternative
        return super(RandomManager, self).get_queryset().order_by('?')

class Game(models.Model):
	WYR = 'WYR'
	TD = 'TD'
	ACT = 'ACT'
	DISC = 'DISC'
	GAME_TYPES = (
		(WYR, 'Would You Rather?'),
		(TD, 'Truth or Dare'),
		(ACT,'Activity'),
		(DISC,'Discuss')
	)
	type = models.CharField(choices=GAME_TYPES, max_length=10, default=DISC)
	text = models.CharField(max_length=500)
	min_players = models.IntegerField(default=2)
	max_players = models.IntegerField(default=maxsize)
	objects = models.Manager()
	random = RandomManager()
=======

class GameType(models.Model):
    types_list = (
        ('WUR', 'Would You Rather...?'),
        ('TOD', 'Truth or Dare'),
        ('ACT', 'Activity'),
        ('DIS', 'Discuss'),
        ('OTH', 'Other')
    )
    game_type = models.CharField(max_length=3, choices=types_list)
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
>>>>>>> da4b183bf1aa60df1094ce0673e7c9ff3ba83ef0
