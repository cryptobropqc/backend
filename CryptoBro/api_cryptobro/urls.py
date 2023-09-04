from django.urls import include, path
from rest_framework import routers

from api_cryptobro.views import PostViewSet, CommentViewSet


app_name = 'api_cryptobro'



router_v1 = routers.DefaultRouter()
router_v1.register("posts", PostViewSet, basename="posts")
router_v1.register("comments", CommentViewSet, basename="comments")



urlpatterns = [
    # path('v1/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]