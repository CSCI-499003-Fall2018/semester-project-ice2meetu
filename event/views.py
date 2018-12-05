from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required
from IceToMeetYou.API.api import EventSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from Home.forms import Join

@login_required(login_url='login/')
def event(request, string):
    event = Event.objects.get(access_code=string)
    user = EventUser.objects.create(user=request.user)
    user.events.add(event)
    user.save()
    return render(request, "event/event.html", context={'event': event })


@api_view(['GET', ])
def go(request, string, format=None):
    event = Event.objects.get(access_code=string)
    if format == 'json':
        return Response(EventSerializer(event).data)
    if request.user.is_authenticated :
        return render(request, "event/event.html", context={'event': event})
    else:
        form = Join()
        content = {
            'form': form,
            'name': 'Access Code',
            'user' : request.user
        }
        return render(request, "Home/join.html", content)