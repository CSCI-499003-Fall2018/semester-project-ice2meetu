from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:event_pk>/begin', views.init_game, name='begin'),
    path('<int:event_pk>/add', views.add_self, name='add_self'),
    path('<int:event_pk>/add_all', views.add_all, name='add_all'),
    path('<int:event_pk>/remove', views.remove_self, name='remove_self'),
    path('<int:event_pk>/end', views.end_game, name='end_game')
]

