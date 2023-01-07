from django.urls import path
from api.services.views import PostCommentAPIView, create_rating_view

urlpatterns = [
    path("rating/<id>/", create_rating_view, name="rate-post"),
    path("comment/<id>/", PostCommentAPIView.as_view(), name="comments"),
]
