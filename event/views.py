from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, EventUser
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def event(request, pk):
    event = Event.objects.get(pk=pk)
    user = EventUser.objects.create(user=request.user)
    user.event.add(event)
    user.save()
    return render(request, "event/event.html", context={'event': event })

