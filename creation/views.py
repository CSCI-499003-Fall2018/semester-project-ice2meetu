from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import EventForm
from .models import Event, EventUser
from .utils import genAccessCode
from django.contrib.auth.decorators import login_required

@login_required(login_url='../login/')
def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_date = timezone.now()
            event.access_code = genAccessCode()
            event.admin = request.user
            event.save()

            return HttpResponseRedirect('../event/{}'.format(event.pk))
           
    else:
        form = EventForm()
    return render(request, "creation/create.html", {'form' : form})
