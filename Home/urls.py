from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home_creation_page"),

    path('signup/', views.signup, name="sign_up_page"),
    path('login/', views.login, name="login_page"),
    path('game', views.game, name="game"),
    path('join', views.join, name="join_page"),
]
