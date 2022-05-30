from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from chatapp.models import Message, Room


@login_required
def rooms(request):
    rooms = Room.objects.all()

    context = {
        'title': 'Комнаты',
        'rooms': rooms,
    }

    return render(request, 'chatapp/rooms.html', context)


@login_required
def room(request, slug):
    rooms = Room.objects.all()
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    context = {
        'title': room.slug,
        'rooms': rooms,
        'room': room,
        'messages': messages
    }

    return render(request, 'chatapp/room.html', context)
