from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home_creation_page"),
    path('signup', views.signup, name="sign_up_page"),
    path('game', views.game, name="game")
]
