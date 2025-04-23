from django import forms
from django.forms import ModelForm

from core.admin import User
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        # Add placeholders
        self.fields["name"].widget.attrs.update(
            {"placeholder": "Enter your room name...", "class": "form__input"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "placeholder": "Write a description about your room...",
                "class": "form__input",
            }
        )


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "username", "bio", "email", "first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Enter new first name..."}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Enter new last name..."}
            ),
            "username": forms.TextInput(attrs={"placeholder": "Enter new username..."}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter new email..."}),
            "bio": forms.Textarea(attrs={"placeholder": "Tell us about yourself..."})
        }
