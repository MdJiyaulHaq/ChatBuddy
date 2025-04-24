import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        room_id = data["room_id"]

        # Save message to database
        await self.save_message(message, room_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_id": self.scope["user"].id,
                "username": self.scope["user"].username,
                "avatar_url": (
                    self.scope["user"].avatar.url if self.scope["user"].avatar else None
                ),
            },
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user_id": event["user_id"],
                    "username": event["username"],
                    "avatar_url": event["avatar_url"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, message, room_id):
        room = Room.objects.get(id=room_id)
        Message.objects.create(user=self.scope["user"], room=room, body=message)
        room.participants.add(self.scope["user"])
