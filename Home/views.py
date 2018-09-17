from django.shortcuts import render

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
