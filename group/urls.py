from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.same_group, name='same_group_page'),
]
