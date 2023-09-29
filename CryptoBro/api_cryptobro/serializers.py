from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from posts.models import Post, Comment, Group
from users.models import User
from users.validators import UsernameValidatorRegex


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для аутентификации пользователей."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # поле "password" будет доступно только для записи 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля пользователя."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
           model = User
           fields = ('old_password', 'new_password')

    def validate(self, data):
        """Проверка что старый пароль должен отличаться от нового."""
        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError("Новый пароль не должен совпадать со старым!")
        return data


class SignUpSerializer(serializers.Serializer):
    """Сериализатор формы регистрации.POST-запрос: username и email."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UsernameValidatorRegex(),],
    )
            
    email = serializers.EmailField(
        max_length=150,
        required=True,
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
