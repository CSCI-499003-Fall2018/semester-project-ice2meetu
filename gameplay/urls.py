from django.urls import path, include
from . import views

urlpatterns = [
    path('playtest', views.play_test, name='play_test')
]

