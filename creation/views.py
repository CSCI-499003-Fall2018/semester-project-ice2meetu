from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import EventForm
from .models import Event
import random
import string

def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            print(request)
            event.created_date = timezone.now()
            rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
            code = rand_str(8)
            
            e_code = Event.objects.filter(access_code=code)
            if len(e_code) > 0:
                while len(e_code) != 0:
                    code = rand_str(8)
                    e_code = Event.objects.filter(access_code=code)
            event.access_code = code

            event.save()
            return HttpResponseRedirect('../event/{}'.format(event.pk))
           
    else:
        form = EventForm()
    return render(request, "creation/create.html", {'form' : form})
