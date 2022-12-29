from django.urls import path
from api.post.views import PostCreateAPIView, updatePostApiView,PostDeleteAPIView

urlpatterns = [
    path("create/post/", PostCreateAPIView.as_view(), name="create-post"),
    path("update/<id>/", updatePostApiView, name="update-post"),
    path("delete/<pkid>/", PostDeleteAPIView.as_view(), name="delete-post"),
]