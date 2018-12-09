from django.urls import path, include, re_path
from . import views
# from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('<int:pk>/', views.event, name='event_page'),
    path('<int:pk>/join', views.join_event, name='join_event')
    # re_path(r'^(?P<string>\w+)/join/$', views.event, name='event_page'),
    # re_path(r'^(?P<string>\w+)/go/$', views.go ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
