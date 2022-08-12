from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder' : 'Имя'}),
            'body': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=250)