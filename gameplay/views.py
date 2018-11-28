from django.shortcuts import render

# Create your views here.


#@login_required(login_url='login/')
def play_test(request):
    return JsonResponse({})
    # if request.user.eventuser_set.exists():
    #     user = list(request.user.eventuser_set.all())[0]
    # else:
    #     raise RuntimeError("Not an event user")
    # if user.events.filter(is_playing=True).exists():
    #     event = list(user.events.filter(is_playing=True))[0]
    # else:
    #     raise RuntimeError(
    #         "User {} is not part of any event".format(repr(user)))
    # s = SimulatedAnnealing(event)
    # grouper = s.generate()
    # grouping = next(grouper)
    # start_games(s.start_state)
    # context = {'event': repr(event),
    #            'groups': []}
    # for group in s.start_state.groups():
    #     info = {}
    #     info['name'] = repr(group)
    #     info['users'] = [repr(user) for user in group.users()]
    #     info['game'] = repr(group.game)
    #     context['groups'].append(info)
    # return JsonResponse(context)
