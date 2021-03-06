from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required
from IceToMeetYou.API.api import EventSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.views.decorators.cache import never_cache
from django.template.response import TemplateResponse

from Home.forms import Join

@login_required(login_url='login/')
def event(request, string):
    event = Event.objects.get(access_code=string)
    user = EventUser.objects.create(user=request.user)
    user.events.add(event)
    user.save()
    return TemplateResponse(request, "event/event.html", context={'event': event, 'join': True })


@api_view(['GET', ])
@permission_classes([AllowAny],)
@never_cache
def go(request, string, format=None):
    event = Event.objects.get(access_code=string)
    if format == 'json':
        return Response(EventSerializer(event).data)

    if request.user.is_authenticated:
        user = event.event_users.filter(user=request.user)

        player = ""
        if hasattr(event, 'gamemanager'):
            player = event.gamemanager.player_set.filter(user__in=user)
        joined = False
        if player != "":
            joined = True
        if joined and len(player) == 0:
            joined = False

        grouping = event.grouping_set.all()
        group = grouping
        content = {
            'event' : event,
            'group' : group,
            'user'  :request.user,
            'join': not joined
        }
        return TemplateResponse(request, "event/event.html", content)
    else:
        form = Join()
        content = {
            'form': form,
            'name': 'Access Code',
            'user' : request.user
        }
    return TemplateResponse(request, "Home/join.html", content)