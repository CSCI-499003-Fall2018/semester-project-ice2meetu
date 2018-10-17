import requests

from .forms import SignUpForm, Join
import random

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

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

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'Home/signup.html', {'form': form})

def logon(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username', '').strip(),
            password= request.POST.get('password', ''),
        )

        if user is None:
            messages.error(request, u'Invalid credentials')
        else:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                messages.error(request, u'User is not active.')

                return render_to_response('Home/login.html', locals(),
                    context_instance=RequestContext(request))
    else:
        return render(request, 'Home/login.html', {})

def game(request): #, nplayers=None):
    # if not nplayers:
    #     return render(request, 'Home/game.html', {'selected': False})
    # min_games = Game.objects.filter(game_type__min_players__gte=nplayers)
    # filtered_games = Game.objects.filter(game_type__max_players__lte=nplayers)
    # rand_game = random.choice(filtered_games)
    # context = {
    #     'text': rand_game.text,
    #     'game': rand_game.game_type.get_game_type_display(),
    #     'selected': True
    # }
    return render(request, 'Home/game.html')#, context)

