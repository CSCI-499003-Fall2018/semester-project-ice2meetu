from django.urls import path, include, re_path
from . import views
# from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    # path('<string>/join/', views.event, name='event_page'),
    # path('<string>/go/', views.go)
    re_path(r'^(?P<string>\w+)/join/$', views.event, name='event_page'),
    re_path(r'^(?P<string>\w+)/go/$', views.go ),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
