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
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder' : 'никнейм'}),
            'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя'}),
            'email' : forms.EmailInput(attrs={'placeholder' : 'Почта'})
        }
        labels = {
            'username' : 'никнейм',
            'first_name' : 'имя',
            'email' : 'почта'
        }


class ProfilEditForm(forms.ModelForm):

    remove_photo = forms.BooleanField(required=False)
    class Meta:
        model = Profile
        fields = ['image', 'status']
        widgets = {
            'image' : forms.FileInput(attrs={'placeholder' : 'фото профиля'}),
            'status': forms.TextInput(attrs={'placeholder': 'статус'})
        }

