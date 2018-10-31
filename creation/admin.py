from django.contrib import admin

from .models import Event, EventUser, Group

# Register your models here.

admin.site.register(Event)
admin.site.register(Group)

admin.site.register(EventUser)