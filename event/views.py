from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required
from IceToMeetYou.API.api import EventSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny

from Home.forms import Join

# Admin must
# init game (turn all users into players, or have users check in)
# start round (create groupings, match groups -> indicate group is found -> game renders)

@login_required(login_url='login/')
def event(request, pk):
    event = Event.objects.get(pk=pk)
    user = event.event_users.get(user__username = request.user.username)
    print(user)
    return render(request, "event/event.html", context={'event': event, 'user': user})

def join_event(request, pk, format=None):
    event = Event.objects.get(pk=pk)
    if format == 'json':
        return Response(EventSerializer(event).data)

    if request.user.is_authenticated :
        event = Event.objects.get(pk=pk)
        user, created = EventUser.objects.get_or_create(user=request.user)
        try:
            user.events.get(pk=pk)
        except Event.DoesNotExist:
            user.events.add(event)
            user.save()
        return HttpResponseRedirect('/event/{}'.format(event.pk))
    else:
        form = Join()
        content = {
            'form': form,
            'name': 'Access Code',
            'user' : request.user
        }
    return render(request, "Home/join.html", content)

"""
def event(request, string):
    event = Event.objects.get(access_code=string)
    user = EventUser.objects.create(user=request.user)
    user.events.add(event)
    user.save()
    return render(request, "event/event.html", context={'event': event })


@api_view(['GET', ])
@permission_classes([AllowAny],)
def go(request, string, format=None):
    event = Event.objects.get(access_code=string)
    if format == 'json':
        return Response(EventSerializer(event).data)

    if request.user.is_authenticated :
        user = event.event_users.filter(events__event_users__user_id=request.user.id)
        grouping = event.grouping_set.all()
        group = grouping
        print(group)
        content = {
            'event' : event,
            'group' : group
        }
        print(group)
        return render(request, "event/event.html", content)
    else:
        form = Join()
        content = {
            'form': form,
            'name': 'Access Code',
            'user' : request.user
        }
    return render(request, "Home/join.html", content)
"""
