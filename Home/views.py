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
    context = {
        'creators': creators,
        'title': 'IceToMeetYou'
    }
    return render(request, 'Home/home.html', context)

def signup(request):
    return render(request, 'Home/signup.html', {})