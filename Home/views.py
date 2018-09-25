from django.shortcuts import render
import requests

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
    return render(request, 'Home/signup.html', {})

def game(request):
    tunnel = "3d0b7810"

    def get_game():
        url = "http://{}.ngrok.io/".format(tunnel)
        response = requests.get(url)
        return response.json()

    context = get_game()
    return render(request, 'Home/game.html', context)
