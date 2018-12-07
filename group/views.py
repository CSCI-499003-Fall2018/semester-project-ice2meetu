from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect, JsonResponse

@login_required(login_url='login/')
def same_group(request):
    # def get_num_groups(request):
    #     if not request.user.eventuser_set.exists():
    #         return None
    #     user = request.user.eventuser_set.all()[0]
    #     event = user.player.game_manager.event
    #     grouping = event.gamemanager.get_current_grouping()
    #     return grouping.group_set.count()

    def get_group_id(request):
        if not request.user.eventuser_set.exists():
            return None
        user = request.user.eventuser_set.all()[0]
        event = user.player.game_manager.event
        grouping = event.gamemanager.get_current_grouping()

        for group in grouping.groups():
            if user in group.users():
                return group.pk
    
        return None
    
    def get_group_pos(request):
        if not request.user.eventuser_set.exists():
            return None
        user = request.user.eventuser_set.all()[0]
        event = user.player.game_manager.event
        grouping = event.gamemanager.get_current_grouping()
        position = 0

        for group in grouping.groups():
            position += 1
            if user in group.users():
                return position%30
    
        return None

    def get_num_people(request):
        if not request.user.eventuser_set.exists():
            return None
        
        group_id = get_group_id(request)
        user = request.user.eventuser_set.all()[0]
        event = user.player.game_manager.event
        grouping = event.gamemanager.get_current_grouping()
        
        for group in grouping.groups():
            if group.pk == group_id:
                return group.size()

        return None

    def generate_color():
        color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
        return color

    context = {
        "group_number": get_group_pos(request),
        "number_of_people": get_num_people(request),
        "color": generate_color(),
    }

    return render(request, "group/group.html", context)
