from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .models import Game

# Create your views here.
def games(request):
	rand_obj = Game.random.values()[0]
	return JsonResponse(rand_obj)