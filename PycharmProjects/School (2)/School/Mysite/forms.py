from django import forms
from django.forms import ModelForm

from Mysite.models import Comments

class CommentsForm(ModelForm):
    class Meta:
        model=Comments
        fields=['name','text']
