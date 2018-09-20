from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.create, name="creation_page"),
    path('addForm', views.addForm, name="addForm")
]
