from django.contrib import admin
<<<<<<< HEAD
from .models import Game

# Register your models here.
admin.site.register(Game)
=======
from .models import Game, GameType

# Register your models here.
admin.site.register(Game)
admin.site.register(GameType)
>>>>>>> da4b183bf1aa60df1094ce0673e7c9ff3ba83ef0
