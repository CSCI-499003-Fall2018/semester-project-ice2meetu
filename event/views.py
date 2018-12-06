from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def event(request, pk):
    event = Event.objects.get(pk=pk)
    user = event.event_users.get(user__username = request.user.username)
    print(user)
    return render(request, "event/event.html", context={'event': event, 'user': user})

@login_required(login_url='login/')
def join_event(request, pk):
    event = Event.objects.get(pk=pk)
    user, created = EventUser.objects.get_or_create(user=request.user)
    try:
        user.events.get(pk=pk)
    except Event.DoesNotExist:
        user.events.add(event)
        user.save()
    return HttpResponseRedirect('/event/{}'.format(event.pk))


# Admin must
# init game (turn all users into players, or have users check in)
# start round (create groupings, match groups -> indicate group is found -> game renders)