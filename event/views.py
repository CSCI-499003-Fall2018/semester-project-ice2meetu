from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event 

def event(request, pk):
    event = Event.objects.get(pk=pk)
    user = True
    print(event.admin)
    return render(request, "event/event.html", context={'event': event , 'user': user})

