from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import EventForm

def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            print(request)
            event.created_date = timezone.now()
            form
            event.save()
            return HttpResponseRedirect('../event/{}'.format(event.pk))
           
    else:
        form = EventForm()
    return render(request, "creation/create.html", {'form' : form})