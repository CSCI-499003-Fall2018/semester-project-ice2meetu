from django.shortcuts import render
import requests
from .forms import UserCreationForm

creators = [
    {
        'name' : 'Kevin',
        'school': 'Hunter College'
    },
    {
        'name' : 'Dandan',
        'school': 'Hunter College'
    },
    {
        'name' :'Silvena',
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
