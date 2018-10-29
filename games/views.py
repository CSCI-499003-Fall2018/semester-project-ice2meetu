from django.shortcuts import render
from .models import Game
from django.http import HttpResponseRedirect, JsonResponse

def games(request, pk):
    game = Game.objects.get(pk=pk)
    if not request.GET:
        err = {
            'status': 400,
            'id': None,
            'text': 'Please enter number of players',
            'game': None
        }
        return JsonResponse(err)
    context = {
        'status': 200,
        'id': game.id,
        'text': game.text,
        'game': game.game_type.get_game_type_display()
    }
    return JsonResponse(context)
