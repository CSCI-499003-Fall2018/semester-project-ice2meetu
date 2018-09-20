from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def create(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = NameForm()
    return render(request, "creation/create.html", {'form' : form})

def addForm(request):
    print(request.POST)
    if request.method == 'POST':
        form = NameForm(request.POST)
    return render(request, 'creation/create.html', {'form': form})
def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/')
        else:
            form = NameForm()
        return render(request, 'create.html', {'form': form})
# Create your views here.