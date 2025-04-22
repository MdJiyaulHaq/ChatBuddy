from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        # Add placeholders
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter your room name...',
            'class': 'form__input'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Write a description about your room...',
            'class': 'form__input'
        })
