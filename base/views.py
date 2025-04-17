from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from base.forms import RoomForm
from django.db.models import Q
from base.models import Room, Topic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def loginPage(request):

    if request.user.is_authenticated:
        return redirect("home")

    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        User = get_user_model()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("home")


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


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}

    if request.user != room.host:
        messages.error(request, "You are not allowed to update this room!")
        return redirect("home")

    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        messages.success(request, "Room was deleted successfully!")
        return redirect("home")

    obj = {"room": room}

    if request.user != room.host:
        messages.error(request, "You are not allowed to delete this room!")
        return redirect("home")

    return render(request, "base/delete_room.html", obj)
