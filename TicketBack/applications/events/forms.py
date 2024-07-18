from django import forms
from .models import Event


class CustomEventEditForm(forms.ModelForm):

    class Media:
        js = ('events/my_form.js',)

    class Meta:
        model = Event
        fields = [
            'status',
            'title',
            'slug',
            'counter',
            'price',
            'on_landing',
            'content',
            'expired',
            'image',
            'category',
            'time_event',
            'link',
        ]
