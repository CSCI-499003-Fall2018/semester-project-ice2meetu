from django.db import models

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

class Game(models.Model):
    game_type = models.ForeignKey(GameType, default="",
                             on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    def __str__(self):
        type_str = self.game_type.get_game_type_display()
        return "{}: {}".format(type_str, self.text)
