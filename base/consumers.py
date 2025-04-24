import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import json
from base.models import Room, Message


User = get_user_model()


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["Pk"]
        self.room_group_name = f"room_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        # Close the connection
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user_id = data["user_id"]
        room_id = self.room_id

        # Save the message to the database
        await self.save_message(user_id, room_id, message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_id": user_id,
                "timestamp": str(datetime.datetime.now()),
            },
        )
