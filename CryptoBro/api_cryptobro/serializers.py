from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from posts.models import Post, Comment, Group
from users.models import User
from users.validators import UsernameValidatorRegex
 


class SignUpSerializer(serializers.Serializer):
    """Сериализатор формы регистрации.POST-запрос: username и email."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UsernameValidatorRegex(),],
    )
            
    email = serializers.EmailField(
        required=False,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def validate(self, data):
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')):
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения JWT-токена."""
    username = serializers.CharField(
        required=True,
        validators=[UnicodeUsernameValidator, ]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code') 


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        # read_only_fields = ('role',)



class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Group
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='username'
    )
    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)
