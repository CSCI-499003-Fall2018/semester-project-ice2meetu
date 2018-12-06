from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect, JsonResponse

@login_required(login_url='login/')
def same_group(request):
    def get_group_id(request):
        if not request.user.eventuser_set.exists():
            return None
        user = request.user.eventuser_set.all()[0]
        event = user.player.game_manager.event
        grouping = event.game_manager.get_current_grouping()

        for group in grouping.groups():
            if user in group.users():
                group_id = int('0' + group.pk)
                return group_id
    
        return None

    context = {
        "group_id": get_group_id(request)
    }

    return render(request, "group/group.html", context)
