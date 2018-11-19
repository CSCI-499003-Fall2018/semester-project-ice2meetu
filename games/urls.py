from django.urls import path, include
from . import views
# from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.game, name='game'),
    path('<int:pk>/', views.gamesid, name='game_api'),
    path('random', views.get_nplayer_game, name="get_game"),
    path('event', views.get_user_game, name='get_user_game'),
    path('playtest', views.play_test, name='play_test')
]
