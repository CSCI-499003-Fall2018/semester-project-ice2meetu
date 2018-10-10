"""IceToMeetYou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home_creation_page"),
    path('login/', auth_views.LoginView.as_view(template_name="Home/login.html"), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view, {'next_page': '/'}, name='logout_page'),
    path('signup', views.signup, name="sign_up_page"),
    path('game', views.game, name="game"),
    path('get_game', views.get_nplayer_game, name="get_game"),
    path('join', views.join, name="join_page")
]
