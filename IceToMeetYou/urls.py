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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from IceToMeetYou.API.api import UserViewSet, EventViewSet, GameViewSet, GroupingViewSet, GroupViewSet
from IceToMeetYou.API.auth_api import CustomAuthToken


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('events', EventViewSet)
router.register('games', GameViewSet)
router.register('grouping', GroupingViewSet)
router.register('group', GroupViewSet)

urlpatterns = [
    url(r'^', include(('Home.urls', 'Home'), namespace='Home')),

    path('', include('Home.urls')),
    path('create/', include('creation.urls')),
    path('event/', include('event.urls')),
    path('games/', include('games.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),  # <-- Social Login
    path('api-auth/', CustomAuthToken.as_view()),
    path('api/', include(router.urls))
]
