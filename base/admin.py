from django.contrib import admin
from .models import Room
from django.contrib import admin
from django.contrib.admin import ModelAdmin


# Register your models here.
@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "updated", "created")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_filter = ("updated", "created")
    list_per_page = 10
    ordering = ("-updated",)
    readonly_fields = ("created", "updated")
