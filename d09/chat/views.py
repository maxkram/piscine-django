from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

def chat_index(request):
    # Ensure rooms exist
    for name in ['Room1', 'Room2', 'Room3']:
        ChatRoom.objects.get_or_create(name=name)
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def chat_room(request, room_name):
    room = ChatRoom.objects.get(name=room_name)
    return render(request, 'chat/room.html', {'room_name': room.name})