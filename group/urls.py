from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('group', views.same_group, name='same_group_page'),
]
