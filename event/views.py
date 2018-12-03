from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required
from IceToMeetYou.API.api import EventSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view

@login_required(login_url='login/')
def event(request, string):
    event = Event.objects.get(access_code=string)
    user = EventUser.objects.create(user=request.user)
    user.events.add(event)
    user.save()
    return render(request, "event/event.html", context={'event': event })


@api_view(['GET', ])
def go(request, string, format=None):
    print(string)
    event = Event.objects.get(access_code=string)
    print(format)
    if format == 'json':
        return Response(EventSerializer(event).data)
    return render(request, "event/event.html", context={'event': event})