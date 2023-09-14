from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from CryptoBro.settings import EMAIL_HOST

from .permissions import IsAdminOrReadOnly, IsAdmitOrGetOut, IsAuthorOrReadOnly
from .serializers import (
    UsersSerializer,
    SignUpSerializer,
    TokenSerializer,
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    
)

from posts.models import Post, Comment, Group
from users.models import User



class SignUpViewSet(APIView):
    """Регистрация."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        send_mail(
            subject='Код подтверждения',
            message=(f'Ваш confirmation_code: {user.confirmation_code}'),
            from_email=EMAIL_HOST,
            recipient_list=[request.data.get('email')],
            fail_silently=False,
        )
        user.save()
        return Response(
            serializer.data, status=HTTP_200_OK
        )


class TokenViewSet(APIView):
    """Получение токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if str(user.confirmation_code) == request.data.get(
                'confirmation_code'
        ):
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(
                token, status=HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения.'},
            status=HTTP_400_BAD_REQUEST
        )



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=username",)
    lookup_field = "username"

    def perform_create(self, serializer):
        if self.request.user.role == "admin":
            if not self.request.POST.get("email"):
                raise ValidationError("entry is already exist.")
        serializer.save()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return (IsAdmitOrGetOut(),)
        return super().get_permissions()

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        # url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == "GET":
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UsersSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)



class PostViewSet(viewsets.ModelViewSet):
    """Доступ: Аутентификация. Автор редактирует или только чтение."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
   

class CommentViewSet(viewsets.ModelViewSet):
    """Доступ к комментариям: Аутентификация."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """Cоздание комментария к посту."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        """Переопределяем метод представления get_queryset."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()
