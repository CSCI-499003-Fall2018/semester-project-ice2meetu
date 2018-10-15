from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event 

def event(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, "event/event.html", context={'event': event})

