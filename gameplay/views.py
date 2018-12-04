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

# Game Admin Endpoints #

def check_authed_admin(request, event):
    if not event.exists():
        err = {"Error": "Event id {} doesn't exist".format(event_pk)}
        return (404, err)
    if request.user != event[0].admin:
        msg = "You're not the admin of this event"
        err = {"Unauthorized Error": msg}
        return (401, err)
    return (200, {"Success":""})

@login_required(login_url='login/')
def init_game(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_authed_admin(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)
    
    if event.is_playing:
        return JsonResponse({"Error": "This event is already playing"})
    if not hasattr(event, 'gamemanager'):
        manager = GameManager.objects.create(event=event)
    return JsonResponse({"Success": "Game Manager Created"})


@login_required(login_url='login/')
def end_game(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_authed_admin(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)

    if not event.is_playing and not hasattr(event, 'gamemanager'):
        return JsonResponse({"Error": "This event is not playing"})

    event.gamemanager.end_game()
    return JsonResponse({"Success": "Game was ended"})


@login_required(login_url='login/')
def add_all(request, event_pk):
    event=Event.objects.filter(pk = event_pk)
    status, err=check_authed_admin(request, event)
    if status == 200:
        event=event[0]
    else:
        return JsonResponse(status = status, data = err)

    event.gamemanager.sync_users()
    players = list(event.gamemanager.players())
    return JsonResponse({"Success": "All Event Users added",
                         "Player IDs": players})


# Game Player Endpoints #

def check_event_user(request, event):
    if not event.exists():
        err = {"Error": "Event id {} doesn't exist".format(event_pk)}
        return (404, err)
    event_user = request.user.eventuser_set.all()[0]
    if event[0] not in event_user.events.all():
        msg = "You're participating in this event"
        err = {"Unauthorized Error": msg}
        return (401, err)
    if not GameManager.objects.filter(event=event[0]).exists():
        msg = "This game has not been opened for joining yet"
        err = {"Unauthorized Error": msg}
        return (401, err)
    return (200, {"Success": event_user})

@login_required(login_url='login/')
def add_self(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_event_user(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)
    
    event_user = err['Success']
    manager = GameManager.objects.filter(event=event)[0]
    manager.add_player(event_user)
    return JsonResponse({"Success": "You've been added to the game"})


@login_required(login_url='login/')
def remove_self(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_event_user(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)

    event_user = err['Success']
    event_user.player.remove_self()
    return JsonResponse({"Success": "You've been removed from the game"})

    


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
