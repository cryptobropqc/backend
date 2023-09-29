from django.urls import include, path
from rest_framework import routers

from api_cryptobro.views import (SignUpViewSet, TokenViewSet, UserViewSet,
                                 PostViewSet, CommentViewSet, GroupViewSet,
                                 RegisterUser, UserLogin, UserLogout, 
                                 ChangePasswordAPIView)
                               


app_name = "api_cryptobro"


router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("groups", GroupViewSet, basename="groups")
router.register(r"users", UserViewSet, basename="users")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", SignUpViewSet.as_view(), name='signup'),
    path("auth/token/", TokenViewSet.as_view(), name='token'),
    # Новая авторизация, регистрация, и выход из системы c удалением токена
    path('auth/register/', RegisterUser.as_view(), name='register'),
    path('auth/login/', UserLogin.as_view(), name='login'),
    path('auth/logout/', UserLogout.as_view(), name='logout'),
    path('auth/change_password/', ChangePasswordAPIView.as_view(), name='change_password'),
]