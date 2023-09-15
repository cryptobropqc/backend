from django import forms
from django.forms import ModelForm, TextInput

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title','text', 'group', 'image')
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название поста'
            }),
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
            'image': 'Картинка к посту',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Добавить комментарий'}
        help_texts = {'text': 'Текст комментария'}
