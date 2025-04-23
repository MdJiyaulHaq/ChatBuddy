from django.contrib import admin
from .models import Room, Message, Topic
from django.contrib.admin import ModelAdmin


# Register your models here.
@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ("id", "name", "topic", "host", "description", "updated", "created")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_filter = ("updated", "created")
    list_per_page = 10
    ordering = ("-updated",)
    readonly_fields = ("created", "updated")


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("id", "room", "user", "body", "updated", "created")
    list_display_links = ("id", "room")
    search_fields = ("room__name", "user__username", "body")
    list_filter = ("updated", "created")
    list_per_page = 10
    ordering = ("-updated",)
    readonly_fields = ("created", "updated", "room", "user", "body")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True  # Keeping delete permission to remove inappropriate messages if needed


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ("id", "name", "updated", "created")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("updated", "created")
    list_per_page = 10
    ordering = ("-updated",)
    readonly_fields = ("created", "updated")
