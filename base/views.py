from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from base.forms import RoomForm
from core.forms import CustomUserCreationForm
from django.db.models import Q
from base.models import Message, Room, Topic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def registerPage(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context=context)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect("home")

    page = "login"
    if request.method == "POST":
        username = request.POST.get("username").lower()
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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=querry))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": rooms.count(),
        "q": querry,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message_body = request.POST.get("body")
        if message_body:
            room.message_set.create(
                user=request.user,
                room=room,
                body=message_body,
            )
            room.participants.add(request.user)
            return redirect("room", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
        "room_count": rooms.count(),
    }
    return render(request, "base/profile.html", context)


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


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = get_object_or_404(Message, pk=pk)
    room_id = message.room.id

    if request.user != message.user:
        messages.error(request, "You are not allowed to delete this message!")
        return redirect("room", pk=room_id)

    if request.method == "POST":
        message.delete()
        messages.success(request, "Message was deleted successfully!")
        return redirect("room", pk=room_id)

    context = {"obj": message}
    return render(request, "base/delete_message.html", context)
