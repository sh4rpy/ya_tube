from django import forms

from .models import Post, Group, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'group']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'description', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
