from django.urls import path
from api.services.views import create_rating_view

urlpatterns = [
    path("rating/<id>/", create_rating_view, name="rate-post")
]
