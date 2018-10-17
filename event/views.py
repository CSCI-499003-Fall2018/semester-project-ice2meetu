from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from creation.models import Event, Group, User
from Home.forms import Join

def join(request):
    if request.method == 'POST':
        form = Join(request.POST)
        try:
            print(form.data['name'], "\n")
            code = form.data['access_code']
            event = Event.objects.get(access_code=code)
        except ObjectDoesNotExist:
            content = {
                'form': form,
                'name': 'Invalid Access Code'
            }
            return render(request, 'Home/join.html', content)
        g = Group.objects.filter(curr_size__lt = 4)[0]
        g.curr_size += 1
        g.save()
        u = User(group = g, name = form.data['name'])
        u.save()
        return HttpResponseRedirect('../event/{}'.format(event.pk))

    else:
        form = Join()
    content = {
        'form': form,
        'name': 'Access Code'
    }
    return render(request, 'Home/join.html', content)

def event(request, pk):
    event = Event.objects.get(pk=pk)
    # create user object to 
    return render(request, "event/event.html", context={'event': event})

