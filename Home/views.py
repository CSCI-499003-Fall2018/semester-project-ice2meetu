from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Join
from creation.models import Event
from django.core.exceptions import ObjectDoesNotExist
import requests
from .forms import UserCreationForm

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Home')
    else:
        form = UserCreationForm()
    return render(request, 'Home/signup.html', {'form': form})

def login(request):
    return render(request, 'Home/login.html', {})


def game(request, nplayers=None):
    if not nplayers:
        return render(request, 'Home/game.html', {'selected': False})
    filtered_games = Game.objects.filter(game_type__num_players__exact=nplayers)
    rand_game = random.choice(filtered_games)
    context = {
        'text': rand_game.text,
        'game': rand_game.game_type.get_game_type_display(),
        'selected': True
    }
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
