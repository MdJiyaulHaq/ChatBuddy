from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from base.forms import RoomForm, UserForm
from core.forms import CustomUserCreationForm
from django.db.models import Q
from base.models import Message, Room, Topic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync


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
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        User = get_user_model()
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Email or password is incorrect")

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
        rooms = Room.objects.select_related("topic").all()[:5]

    topics = Topic.objects.all()[:6]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=querry))[:5]

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
        body = request.POST.get("body")
        uploaded_file = request.FILES.get("file")

        if body or uploaded_file:
            Message.objects.create(
                user=request.user,
                room=room,
                body=body if body else "",
                file=uploaded_file if uploaded_file else None,
            )
            room.participants.add(request.user)

            channel_layer = get_channel_layer()
            event = {
                "type": "chat_message",
                "message": body or uploaded_file.name,
            }
            async_to_sync(channel_layer.group_send)(f"room_{room.pk}", event)

            return redirect("room", pk=room.id)
        else:
            messages.error(request, "Cannot send an empty message.")

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
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host == request.user
        #     room.save()
        #     return redirect("home")
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect("home")
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}

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

    return render(request, "base/delete.html", obj)


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
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User profile updated successfully!")
            return redirect("user-profile", pk=user.id)

    context = {"form": form}
    return render(request, "base/update-profile.html", context)


@login_required(login_url="login")
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "base/password_change.html", {"form": form})


def topicsPage(request):
    topics = Topic.objects.all()
    querry = request.GET.get("q", "")
    if querry:
        topics = topics.filter(name__icontains=querry)

    context = {"topics": topics, "q": querry}
    return render(request, "base/topics.html", context)


def activityPage(request):
    room_messages = Message.objects.all()
    querry = request.GET.get("q", "")
    if querry:
        room_messages = room_messages.filter(
            Q(room__topic__name__icontains=querry)
            | Q(room__name__icontains=querry)
            | Q(user__username__icontains=querry)
        )

    context = {"room_messages": room_messages, "q": querry}
    return render(request, "base/activity.html", context)
