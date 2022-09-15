import os

from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder' : 'Никнейм'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Почты'}),
        }

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != self.cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password1']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        # widgets = {
        #     'username' : forms.TextInput(attrs={'placeholder' : 'никнейм'}),
        #     'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя'}),
        #     'email' : forms.EmailInput(attrs={'placeholder' : 'Почта'})
        # }
        labels = {
            'username' : 'Никнейм',
            'first_name' : 'Имя',
            'email' : 'Почта'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


class ProfilEditForm(forms.ModelForm):

    remove_photo = forms.BooleanField(required=False)
    class Meta:
        model = Profile
        fields = ['image', 'status', 'tags']
        widgets = {
            'image' : forms.FileInput(attrs={'placeholder' : 'Фото профиля'}),
            'status': forms.TextInput(attrs={}),
            'tags': forms.TextInput(attrs={'placeholder': 'Теги'})
        }
        labels = {
            'status' : 'Статус'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

