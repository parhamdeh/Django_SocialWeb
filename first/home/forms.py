from django import forms
from .models import Post, Comment

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class CommentCreateForm(forms.ModelForm):
    class Met:
        model = Comment
        fields = ('body', )