from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, JsonResponse
from creation.models import Event, EventUser
from games.models import Game, GameType
from .models import GameManager, Player
from django.template.response import TemplateResponse

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


@never_cache
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


@never_cache
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


@never_cache
@login_required(login_url='login/')
def add_all(request, event_pk):
    event=Event.objects.filter(pk = event_pk)
    status, err=check_authed_admin(request, event)
    if status == 200:
        event=event[0]
    else:
        return JsonResponse(status = status, data = err)

    event.gamemanager.sync_users()
    event.gamemanager.max_groups = 5
    players = list(event.gamemanager.players())
    return JsonResponse({"Success": "All Event Users added",
                         "Player IDs": players})


@login_required(login_url='login/')
@never_cache
def start_round(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_authed_admin(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)
    
    if not event.is_playing and not hasattr(event, 'gamemanager'):
        return JsonResponse({"Error": "This event is not playing"})
    
    manager = event.gamemanager
    if len(manager.players()) < 2:
        return JsonResponse({"Error": "Less than 2 players ready to play"})

    play = manager.go_round()
    if not play:
        return JsonResponse({"Error": "All possible rounds complete"})
    group_objs = manager.get_current_grouping().groups()
    groups = [list(group.users()) for group in group_objs]
    grouped_users = []
    for users_list in groups:
        users = []
        for user in users_list:
            users.append(repr(user))
        grouped_users.append(users)
    return JsonResponse({"Success": "Round {} started".format(manager.round_num),
                         "Groups": grouped_users})

# Game Player Endpoints #

def check_event_user(request, event):
    if not event.exists():
        err = {"Error": "Event id {} doesn't exist".format(event_pk)}
        return (404, err)
    # event_user = request.user.eventuser_set.all()
    event_user = EventUser.objects.filter(user=request.user)
    ret = None
    for e_u in event_user:
        print(e_u.events.all())
        print(event)
        for e in e_u.events.all():
            if event[0].access_code == e.access_code:
               ret = e_u
    if ret == None:
        msg = "You're participating in this event"
        err = {"Unauthorized Error": msg}
        return (401, err)
    if not GameManager.objects.filter(event=event[0]).exists():
        msg = "This game has not been opened for joining yet"
        err = {"Unauthorized Error": msg}
        return (401, err)
    return (200, {"Success": event_user})


@never_cache
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
    player = event.gamemanager.player_set.filter(user__in=event_user)
    player = len(player) == 0
    content = {
        'event' : event,
        'join': player
    }
    return TemplateResponse(request,"event/event.html",content)
    # return JsonResponse({"Success": "You've been added to the game"})



@never_cache
@login_required(login_url='login/')
def remove_self(request, event_pk):
    event = Event.objects.filter(pk=event_pk)
    status, err = check_event_user(request, event)
    if status == 200:
        event = event[0]
    else:
        return JsonResponse(status=status, data=err)

    event_user = err['Success']
    if not isinstance(event_user, EventUser):
        event_user = event_user.filter(events__access_code = event.access_code)[0]
    event_user.player.remove_self()
    # return JsonResponse({"Success": "You've been removed from the game"})

    player = event.gamemanager.player_set.filter(user=event_user)
    player = len(player) == 0
    content = {
        'event' : event,
        'join': player
    }
    return TemplateResponse(request,"event/event.html",content)


    


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
