from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from base.models import Room, Topic, Message
from .serializers import RoomSerializer, TopicSerializer, MessageSerializer
from .permissions import IsHostOrReadOnly, IsMessageAuthorOrReadOnly


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsHostOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsMessageAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
