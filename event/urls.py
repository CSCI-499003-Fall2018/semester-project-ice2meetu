from django.urls import path, include
from . import views
# from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.join, name="join_page"),
    path('<int:pk>/', views.event, name='event_page'),
]
