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
    context = {
        'event_id': 0,
        'event_playing': False,
        'is_playing': False
    }
    try: 
        user = request.user
        if not user.is_authenticated or not user.eventuser_set.exists():
            return render(request, 'Games/game.html', context)
        if user.eventuser_set.exists():
            eventuser = user.eventuser_set.all()[0]
            if eventuser.events.filter(is_playing=True).exists():
                context['event_playing'] = True
                context['event_id'] = eventuser.events.filter(
                    is_playing=True)[0].pk
            if eventuser.is_playing():
                context['event_id'] = eventuser.playing_event().pk
                if eventuser.playing_event().is_playing:
                    context['is_playing'] = True
                    group = eventuser.current_group()
                if not group.is_complete:
                    return HttpResponseRedirect(reverse('same_group_page'))
    except AttributeError:
        pass #AnonUser
    print(context)
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
