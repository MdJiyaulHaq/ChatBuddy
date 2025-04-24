# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Use the relative import as in your original file
from .models import Message, Room
from django.contrib.auth import get_user_model

# Ensure User model is correctly retrieved
User = get_user_model()


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Ensure user is authenticated before proceeding
        # Requires AuthMiddlewareStack in your asgi.py
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["Pk"]
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope["user"]  # Store authenticated user

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        print(
            f"WebSocket connected for user {self.user.username} in room {self.room_id}"
        )  # Optional debug print

    async def disconnect(self, close_code):
        # Leave room group
        print(
            f"WebSocket disconnected for user {self.user.username} in room {self.room_id}"
        )  # Optional debug print
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            username = self.user.username

            # Get avatar URL or fallback to default
            avatar_url = (
                self.user.avatar.url
                if hasattr(self.user, "avatar") and self.user.avatar
                else "/static/images/avatar.svg"  # Use the actual path for your static avatar
            )

            await self.save_message(self.user, self.room_id, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "avatar_url": avatar_url,
                },
            )
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {text_data}")
        except KeyError:
            print(f"Error: 'message' key not found in JSON data: {text_data_json}")
        except Exception as e:
            print(f"An error occurred in receive for user {self.user.username}: {e}")

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        avatar_url = event["avatar_url"]

        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "avatar_url": avatar_url}
            )
        )

    # --- Updated async helper function to save message ---
    @sync_to_async
    def save_message(self, user, room_id, message):
        # Takes the user object directly
        try:
            # Ensure the room exists
            room = Room.objects.get(id=room_id)
            # Create the message
            Message.objects.create(user=user, room=room, body=message)
            print(
                f"Message saved: User '{user.username}', Room '{room_id}'"
            )  # Optional debug print
        except Room.DoesNotExist:
            print(f"Error saving message: Room with id {room_id} does not exist.")
        except Exception as e:
            # Catch other potential errors during save
            print(f"Error saving message for user {user.username}: {e}")

    # ---------------------------------------------
