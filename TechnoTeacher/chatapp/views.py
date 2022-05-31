from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from chatapp.models import Message, Room
from chatapp.forms import RoomForm


@login_required
def rooms(request):
    rooms = Room.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('chat:rooms'))
    else:
        form = RoomForm()

    context = {
        'title': 'Комнаты',
        'rooms': rooms,
        'form': form
    }

    return render(request, 'chatapp/rooms.html', context)


@login_required
def room(request, slug):
    rooms = Room.objects.all()
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('chat:rooms'))
    else:
        form = RoomForm()

    context = {
        'title': room.slug,
        'rooms': rooms,
        'room': room,
        'messages': messages,
        'form': form
    }

    return render(request, 'chatapp/room.html', context)
