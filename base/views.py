from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from base.forms import RoomForm
from base.models import Room


def home(request):
    rooms = get_list_or_404(Room)
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)
