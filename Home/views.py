import requests

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import Join
from .forms import SignUpForm
from creation.models import Event

from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


creators = [
    {
        'name': 'Kevin',
        'school': 'Hunter College'
    },
    {
        'name': 'Dandan',
        'school': 'Hunter College'
    },
    {
        'name': 'Silvena',
        'school': 'Hunter College'
    },
    {
        'name': 'Kristoff',
        'school': 'Hunter College'
    }
]


def home(request):
    args = {
        'title': 'Ice2MeetU'
    }
    return render(request, 'Home/home.html', args)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
           
            username = form.cleaned_data.get['username']
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('Home')
    else:
        form = SignUpForm()
    return render(request, 'Home/signup.html', {'form': form})    

def game(request):
    tunnel = "3d0b7810"

    def get_game():
        url = "http://{}.ngrok.io/".format(tunnel)
        response = requests.get(url)
        if response.status_code != 200:
            return {}
        return response.json()

    context = get_game()
    return render(request, 'Home/game.html', context)


def join(request):
    if request.method == 'POST':
        form = Join(request.POST)
        try:
            code = form.data['access_code']
            form = Event.objects.get(access_code=code)
        except ObjectDoesNotExist:
            content = {
                'form': form,
                'name': 'Invalid Access Code'
            }
            return render(request, 'Home/join.html', content)
        return HttpResponseRedirect('../event/{}'.format(form.pk))

    else:
        form = Join()
    content = {
        'form': form,
        'name': 'Access Code'
    }
    return render(request, 'Home/join.html', content)
