import random2
import string
from asgiref.sync import sync_to_async
from chat.models import Thread


def create_random_string(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random2.choice(chars) for i in range(size))

def unique_room_genarator(instance):
    id = ''
    klass = instance.__class__
    while True:
        id = create_random_string()

        if klass.objects.filter(unique_room_id=id).exists():
            continue
        else:
            break
    
    return id
