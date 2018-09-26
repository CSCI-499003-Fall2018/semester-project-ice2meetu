from .models import Event
import random
import string

# Generates acces code for an Event
def genAccessCode():
    code = rand_str(8)

    e_code = Event.objects.filter(access_code=code)
    if len(e_code) > 0:
        while len(e_code) != 0:
            code = rand_str(8)
            e_code = Event.objects.filter(access_code=code)
    return code


def rand_str(n):
    rand = ''.join([random.choice(string.ascii_lowercase) for i in range(n)])
    return rand
