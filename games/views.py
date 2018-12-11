from django.shortcuts import render
from .models import Game, GameType
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse


@login_required(login_url='../login/')
def get_user_game(request):
    if request.user.eventuser_set.exists():
        user = request.user.eventuser_set.all()[0]
    else:
        raise RuntimeError("Not an event user")
    if user.is_playing():
        game = user.current_game()
        status = 200
        context = {
            'id': game.id,
            'text': game.text,
            'game': game.game_type.get_game_type_display()
        }
    else:
        status = 302
        context = {
            'id': 0,
            'text': "Your Event is not playing right now. If you'd like to \
                    start a random game, please log out and click Start Game.",
            'game': 'Not Playing'
        }
    return JsonResponse(status=status, data=context)

def get_nplayer_game(request):
    if not request.GET:
        status = 400
        err = {
            'id': None,
            'text': 'Please enter number of players',
            'game': None
        }
        return JsonResponse(status=status, data=err)
    nplayers = request.GET.get('nplayers', None)
    filtered_games = Game.objects.nplayer_games(nplayers)
    rand_game = random.choice(filtered_games)
    context = {
        'id': rand_game.id,
        'text': rand_game.text,
        'game': rand_game.game_type.get_game_type_display()
    }
    return JsonResponse(context)

def game(request):
    context = {}
    try: 
        user = request.user
        if not user.is_authenticated or not user.eventuser_set.exists():
            return render(request, 'Games/game.html', context)
        if request.user.eventuser_set.exists():
            for eventuser in request.user.eventuser_set.all():
                if eventuser.is_playing():
                    group = eventuser.current_group()
                    if not group.is_complete:
                        return HttpResponseRedirect(reverse('same_group_page'))
                    context['is_playing'] = True
                    break
    except AttributeError:
        pass #AnonUser
    return render(request, 'Games/game.html', context)

def gamesid(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        err = {
            'text': "Error: Game ID {} does not exist".format(pk)
        }
        return JsonResponse(status=404, data=err)

    context = {
        'id': game.id,
        'text': game.text,
        'game': game.game_type.get_game_type_display()
    }
    return JsonResponse(context)
