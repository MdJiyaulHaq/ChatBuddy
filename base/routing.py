from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/room/<int:Pk>/", RoomConsumer.as_asgi(), name="room"),
]
