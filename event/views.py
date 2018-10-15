from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def event(request, pk):
    event = Event.objects.get(pk=pk)
    user = request.user.is_authenticated()
    print(event.admin)
    return render(request, "event/event.html", context={'event': event , 'user': user})

