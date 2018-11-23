from django.shortcuts import render
from .models import Game, GameType
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect, JsonResponse


@login_required(login_url='login/')
def get_user_game(request):
    if request.user.eventuser_set.exists():
        user = list(request.user.eventuser_set.all())[0]
    else:
        raise RuntimeError("Not an event user")
    if user.events.filter(is_playing=True).exists():
        event = list(user.events.filter(is_playing=True))[0]
    else:
        event = None
    if event:
        game = user.current_game()
        context = {
            'status': 200,
            'id': game.id,
            'text': game.text,
            'game': game.game_type.get_game_type_display()
        }
    else:
        context = {
            'status': 302,
            'id': 0,
            'text': "Your Event is not playing right now. If you'd like to \
                    start a random game, please log out and click Start Game.",
            'game': 'Not Playing'
        }
    return JsonResponse(context)

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
    filtered_games = Game.objects.nplayer_games(nplayers)
    rand_game = random.choice(filtered_games)
    context = {
        'status': 200,
        'id': rand_game.id,
        'text': rand_game.text,
        'game': rand_game.game_type.get_game_type_display()
    }
    return JsonResponse(context)

def game(request):
    context = {'is_playing': False}
    try: 
        if request.user.eventuser_set.exists():
            for eventuser in request.user.eventuser_set.all():
                if eventuser.is_playing():
                    context['is_playing'] = True
            context['is_playing'] = user.is_playing()
    except AttributeError:
        pass #AnonUser
    return render(request, 'Games/game.html', context)

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
