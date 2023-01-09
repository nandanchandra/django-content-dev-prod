from django.urls import path
from api.services.views import FavoriteAPIView, PostCommentAPIView, create_rating_view

urlpatterns = [
    path("rating/<id>/", create_rating_view, name="rate-post"),
    path("comment/<id>/", PostCommentAPIView.as_view(), name="comments"),
    path("favorite/<id>/", FavoriteAPIView.as_view(), name="favorite-posts"),
]
