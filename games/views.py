from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .models import Game, GameType
import random
from django.http import HttpResponseRedirect, JsonResponse

def get_nplayer_game(request):
    if not request.GET:
        err = {
            'status': 400,
            'id': None,
            'text': 'Please enter number of players',
            'game': None
        }
        return JsonResponse(err)
    nplayers = request.GET.get('nplayers', None)
    min_games = Game.objects.filter(game_type__min_players__gte=nplayers)
    filtered_games = Game.objects.filter(game_type__max_players__lte=nplayers)
    rand_game = random.choice(filtered_games)
    context = {
        'status': 200,
        'id': rand_game.id,
        'text': rand_game.text,
        'game': rand_game.game_type.get_game_type_display()
    }
    return JsonResponse(context)

def game(request):
    return render(request, 'Home/game.html')

def gamesid(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        err = {
            'status': 404,
            'text': "Error: Game ID {} does not exist".format(pk)
        }
        return JsonResponse(err)

    context = {
        'status': 200,
        'id': game.id,
        'text': game.text,
        'game': game.game_type.get_game_type_display()
    }
    return JsonResponse(context)