from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrReadOnly, IsAdmitOrGetOut, IsAuthorOrReadOnly
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)

from posts.models import Post, Comment, Group
from users.models import User



class RegisterUser(APIView):
    def post(self, request):
        """Регистрация новых пользователей. 
        Проверка в UserSerializer обязательны полей: 'username', 'email', 'password'"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        """Вход пользователя с использованием токенов аутентификации,
        имя пользователя или пароль. Возвращаем данные о пользователе."""
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if '@' in username:
            user = User.objects.filter(email=username).first()
            username = user.username
            user = authenticate(username=username, password=password)
        if not user:
            user = authenticate(username=username, password=password)
        #if user and not check_password(password, user.password):
        #    user = None
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'email': user.email, 
                            'username': user.username, 
                            'token': token.key}, status=status.HTTP_200_OK)
        return Response({'Error': 'Invalid user credentials!'}, 
                        status=status.HTTP_401_UNAUTHORIZED)


class UserLogout(APIView):
    """Выход авторизованного пользователя из системы, 
    и удаление токена аутентификации пользователя."""
    permissionclasses = [IsAuthenticated]
    def post(self, request):
        try:
            # Удалить токен пользователя для выхода из системы
            request.user.auth_token.delete()
            return Response({'Message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordAPIView(APIView):
    """Изменить пароль. Пользователь должен быть аутентифицирован.
    Проверка в ChangePasswordSerializer валидации данных."""
    permissionclasses = IsAuthenticated
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # обновление сеанса после смены пароля
                return Response({'Message': 'Password changed successfully!'}, status=status.HTTP_200_OK)
            return Response(
                {'Message': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SignUpViewSet(APIView):
#     """Регистрация."""
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user, _ = User.objects.get_or_create(**serializer.validated_data)
#         send_mail(
#             subject='Код подтверждения',
#             message=(f'Ваш confirmation_code: {user.confirmation_code}'),
#             from_email=EMAIL_HOST,
#             recipient_list=[request.data.get('email')],
#             fail_silently=False,
#         )
#         user.save()
#         return Response(
#             serializer.data, status=HTTP_200_OK
#         )


# class TokenViewSet(APIView):
#     """Получение токена."""
#     def post(self, request):
#         serializer = TokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = get_object_or_404(
#             User, username=request.data.get('username')
#         )
#         if str(user.confirmation_code) == request.data.get(
#                 'confirmation_code'
#         ):
#             refresh = RefreshToken.for_user(user)
#             token = {'token': str(refresh.access_token)}
#             return Response(
#                 token, status=HTTP_200_OK
#             )
#         return Response(
#             {'confirmation_code': 'Неверный код подтверждения.'},
#             status=HTTP_400_BAD_REQUEST
#         )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializer(
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
