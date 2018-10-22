from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, Group

def event(request, pk):
    event = Event.objects.get(pk=pk)
    # create user object to 
    return render(request, "event/event.html", context={'event': event})

