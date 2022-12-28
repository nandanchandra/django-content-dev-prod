from django.urls import path
from api.post.views import PostCreateAPIView, updatePostApiView

urlpatterns = [
    path("create/post/", PostCreateAPIView.as_view(), name="create-post"),
    path("update/<id>/", updatePostApiView, name="update-post"),
]