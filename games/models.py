from django.db import models
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