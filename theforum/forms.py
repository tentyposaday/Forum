from django import forms
from . import models


class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'text'] 


class CreateThread(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ['name'] 