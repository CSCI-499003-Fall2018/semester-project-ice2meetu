from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from creation.models import Event, EventUser
from games.models import Game, GameType
from .models import GameManager, Player

#game flow:
# -init: open games to players
# -users add selves
# -start round

@login_required(login_url='login/')
def init_game(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    if not event.exists():
        return JsonResponse({"Error": "Event id {} doesn't exist".format(event_pk)})
    event = event[0]
    if request.user != event.admin:
        return JsonResponse({"Error": "You're not the admin of this event"})
    if event.is_playing:
        return JsonResponse({"Error": "This event is already playing"})

    manager = GameManager.objects.create(event=event)
    return JsonResponse({"Success": "Game Manager Created"})


@login_required(login_url='login/')
def add_all(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    if not event.exists():
        return JsonResponse({"Error": "Event id {} doesn't exist".format(event_pk)})
    event = event[0]
    if request.user != event.admin:
        return JsonResponse({"Error": "You're not the admin of this event"})
    event.gamemanager.sync_users()
    return JsonResponse({"Success": "Game Manager Created"})


@login_required(login_url='login/')
def add_self(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    if not event.exists():
        return JsonResponse({"Error": "Event id {} doesn't exist".format(event_pk)})
    event = event[0]
    event_user = request.user.eventuser_set.all()[0]  # change later
    if event not in event_user.events.all():
        return JsonResponse({"Error": "You are not participating in this event"})
    manager = GameManager.objects.filter(event=event)
    if not manager.exists():
        return JsonResponse({"Error": "This event hasn't been opened yet"})
    manager.add_player(event_user)
    return JsonResponse({"Success": "Game Manager Created"})


@login_required(login_url='login/')
def remove_self(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    if not event.exists():
        return JsonResponse({"Error": "Event id {} doesn't exist".format(event_pk)})
    event = event[0]
    event_user = request.user.eventuser_set.all()[0]
    event_user.player.remove_self()
    return JsonResponse({"Success": "Game Manager Created"})

    


#@login_required(login_url='login/')
# def play_test(request):
    # if request.user.eventuser_set.exists():
    #     user = list(request.user.eventuser_set.all())[0]
    # else:
    #     raise RuntimeError("Not an event user")
    # if user.events.filter(is_playing=True).exists():
    #     event = list(user.events.filter(is_playing=True))[0]
    # else:
    #     raise RuntimeError(
    #         "User {} is not part of any event".format(repr(user)))
    # s = SimulatedAnnealing(event)
    # grouper = s.generate()
    # grouping = next(grouper)
    # start_games(s.start_state)
    # context = {'event': repr(event),
    #            'groups': []}
    # for group in s.start_state.groups():
    #     info = {}
    #     info['name'] = repr(group)
    #     info['users'] = [repr(user) for user in group.users()]
    #     info['game'] = repr(group.game)
    #     context['groups'].append(info)
    # return JsonResponse(context)
