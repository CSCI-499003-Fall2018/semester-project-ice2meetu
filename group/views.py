from django.shortcuts import render
from .models import Game, GameType
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect, JsonResponse

@login_required(login_url='login/')
def same_group(request):
    return render(request, "group/group.html")
