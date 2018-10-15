#import requests

from .forms import SignUpForm, Join
from creation.models import Event
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    print("Here")
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', ''),
        )

        print("Here")
        if user is None:
            print("Here")
            messages.error(request, u'Invalid credentblog.ials')
        else:
            if user.is_active:
                print("Here")
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                messages.error(request, u'User is not active.')

                return render_to_response('Home/login.html', locals(),
                                          context_instance=RequestContext(request))
    else:
        return render(request, 'Home/login.html', {})


def game(request, nplayers=None):
    if not nplayers:
        return render(request, 'Home/game.html', {'selected': False})
    filtered_games = Game.objects.filter(
        game_type__num_players__exact=nplayers)
    rand_game = random.choice(filtered_games)
    context = {
        'text': rand_game.text,
        'game': rand_game.game_type.get_game_type_display(),
        'selected': True
    }
    return render(request, 'Home/game.html', context)

@login_required(login_url='login/')
def join(request):
    if request.method == 'POST' and request.user.is_authenticated:

        form = Join(request.POST)
        try:
            code = form.data['access_code']
            form = Event.objects.get(access_code=code)
        except Event.DoesNotExist:
            content = {
                'form': form,
                'name': 'Invalid Access Code',
                'user' : request.user
            }
            return render(request, 'Home/join.html', content)

        form.user.append(request.user)
        return HttpResponseRedirect('../event/{}'.format(form.pk))
    else:
        form = Join()

    

    content = {
        'form': form,
        'name': 'Access Code',
        'user' : request.user
    }
    return render(request, 'Home/join.html', content)
