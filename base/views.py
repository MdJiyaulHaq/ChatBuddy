from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from base.forms import RoomForm
from django.db.models import Q
from base.models import Room, Topic


def home(request):
    querry = request.GET.get("q", "")

    if querry:
        rooms = (
            Room.objects.select_related("topic")
            .distinct()
            .filter(
                Q(topic__name__icontains=querry)
                | Q(name__icontains=querry)
                | Q(description__icontains=querry)
            )
        )
    else:
        rooms = Room.objects.select_related("topic").all()

    topics = Topic.objects.all()

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": rooms.count(),
        "q": querry,
    }
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


def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        return redirect("home")

    obj = {"room": room}
    return render(request, "base/delete_room.html", obj)
