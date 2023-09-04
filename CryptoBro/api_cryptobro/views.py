from django.shortcuts import get_object_or_404, render
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_cryptobro.serializers import (
    PostSerializer,
    CommentSerializer
    
)

from blog.models import Post, Comment, PublishedManager 
from account.models import Profile


class PostViewSet(viewsets.ModelViewSet):
    """Доступ: Аутентификация. Автор редактирует или только чтение."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



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
        return post.comment.all()
