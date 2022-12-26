from django.urls import path
from api.post.views import PostCreateAPIView

urlpatterns = [
    path("create/post/", PostCreateAPIView.as_view(), name="create-post"),
]