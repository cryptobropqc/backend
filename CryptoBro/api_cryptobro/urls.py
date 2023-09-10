from django.urls import include, path
from rest_framework import routers

from api_cryptobro.views import (SignUpViewSet, TokenViewSet, UserViewSet,
                                 PostViewSet, CommentViewSet, GroupViewSet)


app_name = "api_cryptobro"


router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("groups", GroupViewSet, basename="groups")
# router.register(r'groups/(?P<group_id>\d+)/', GroupViewSet, basename="groups",)
# path('group/<slug:slug>/', views.group_posts, name='group_list'),
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", SignUpViewSet.as_view(), name='signup'),
    path("v1/auth/token/", TokenViewSet.as_view(), name='token'),
    # path('v1/auth/', include(auth_urls))
]