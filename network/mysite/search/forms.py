import os

from django import forms
from django.contrib.auth.models import User

from .models import Search

class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('nickname', 'gender', 'similar')
        widgets = {
            'nickname' : forms.TextInput(attrs={'placeholder'  : 'Поиск'}),

        }