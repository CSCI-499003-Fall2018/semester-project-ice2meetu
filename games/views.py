<<<<<<< HEAD
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .models import Game

# Create your views here.
def games(request):
	rand_obj = Game.random.values()[0]
	return JsonResponse(rand_obj)
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> da4b183bf1aa60df1094ce0673e7c9ff3ba83ef0
