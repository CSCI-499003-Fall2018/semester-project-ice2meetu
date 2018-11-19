from django.contrib import admin

from .models import Event, EventUser, Group, Grouping

class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'users')

    def users(self, obj):
        try:
            users = [eventuser.user.username for eventuser in obj.users()]
        except AttributeError:
            users = []
        return "{} users: {}".format(len(users), users)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'event', 'users')

    def event(self, obj):
        try:
            return obj.grouping.event
        except AttributeError:
            return None
    
    def users(self, obj):
        try:
            return [user for user in obj.eventuser_set.all()]
        except AttributeError:
            return []

class GroupingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'event', 'groups')

    def groups(self, obj):
        return [group for group in obj.group_set.all()]

admin.site.register(Event, EventAdmin)
admin.site.register(Group, GroupAdmin)

admin.site.register(EventUser)
admin.site.register(Grouping, GroupingAdmin)
