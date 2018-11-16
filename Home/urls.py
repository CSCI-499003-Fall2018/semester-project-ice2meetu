from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='Home'),

    path('', views.home, name="home_creation_page"),
    path('login/', auth_views.LoginView.as_view(template_name="Home/login.html"), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(template_name="/"), name='logout_page'),    
    path('signup', views.signup, name="sign_up_page"),
    path('profile', views.profile, name="profile_page"),
    path('game', views.game, name="game"),
    path('get_game', views.get_nplayer_game, name="get_game"),
    path('join', views.join, name="join_page"),

    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
