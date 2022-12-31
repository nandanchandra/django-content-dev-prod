from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.post.models import Post
from api.services.models import Rating
from api.utils.custom_view_exceptions import AlreadyRated, CantRateYourPost


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_rating_view(request, id):
    author = request.user
    post = Post.objects.get(id=id)
    data = request.data
    if post.author == author:
        raise CantRateYourPost
    already_exists = post.post_ratings.filter(rated_by__pkid=author.pkid).exists()
    if already_exists:
        raise AlreadyRated
    elif data["value"] == 0:
        formatted_response = {"detail": "You can't give a zero rating"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        rating = Rating.objects.create(post=post,rated_by=request.user,value=data["value"],review=data["review"])
        rating.save()
        return Response({"success": "Rating has been added"}, status=status.HTTP_201_CREATED)
