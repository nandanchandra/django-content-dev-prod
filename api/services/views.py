from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions, status,generics
from rest_framework.decorators import api_view, permission_classes,renderer_classes

from api.post.models import Post
from api.post.serializers import PostSerializer
from api.services.models import Comment,Rating,Favorite
from api.services.serializers import PostCommentSerializer,FavoriteSerializer
from api.utils.renderers import CustomeJSONRenderer
from api.utils.custom_view_exceptions import AlreadyFavorited, AlreadyRated, CantRateYourPost

@api_view(["POST"])
@renderer_classes([CustomeJSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def create_rating_view(request, id):
    try:
        post = Post.objects.get(pkid=id)
        author = request.user
        data = request.data
        if post.author == author:
            raise CantRateYourPost
        already_exists = post.post_ratings.filter(rated_by__pkid=author.pkid).exists()
        if already_exists:
            raise AlreadyRated
        elif data["value"] == 0:
            return Response("You can't give a zero rating", status=status.HTTP_400_BAD_REQUEST)
        else:
            rating = Rating.objects.create(post=post,rated_by=request.user,value=data["value"],review=data["review"])
            rating.save()
        return Response("Rating has been added", status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        raise NotFound("That post does not exist in our catalog")

class PostCommentAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCommentSerializer
    renderer_classes = [CustomeJSONRenderer]

    def get(self, request, id):
        try:
            post = Post.objects.get(pkid=id)
        except Post.DoesNotExist:
            raise NotFound("That post does not exist in our catalog")
        try:
            comments = Comment.objects.filter(post_id=post.pkid)
        except Comment.DoesNotExist:
            raise NotFound("No comments found")
        serializer = PostCommentSerializer(comments, many=True, context={"request": request})
        return Response({"num_comments": len(serializer.data), "comments": serializer.data})

    def post(self, request, id):
        try:
            post = Post.objects.get(pkid=id)
            comment = request.data
            comment._mutable = True
            comment["post"] = post.pkid
            comment["author"] = request.user.pkid
            serializer = self.serializer_class(data=comment)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            raise NotFound("That post does not exist in our catalog")

    def put(self, request, id):
        try:
            comment = Comment.objects.get(pkid=id)
            data = request.data
            serializer = self.serializer_class(comment, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Comment updated successfully", status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

    def delete(self, id):
        try:
            comment = Comment.objects.get(pkid=id)
            comment.delete()
            return Response("Comment deleted successfully!", status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

class FavoriteAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer
    renderer_classes = [CustomeJSONRenderer]

    def get(self, request):
        Favorites = Favorite.objects.filter(user_id=request.user.id)
        favorite_posts = []
        for favorite in Favorites:
            post = Post.objects.get(pkid=favorite.post.pkid)
            post = PostSerializer(post, context={"post": post.pkid, "request": request}).data
            favorite_posts.append(post)
        favorites = {"my_favorites": favorite_posts}
        return Response(data=favorites, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        post = Post.objects.get(pkid=id)
        user = request.user

        favorite = Favorite.objects.filter(user=user, post=post.pkid).first()

        if favorite:
            raise AlreadyFavorited
        else:
            data["post"] = post.pkid
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["message"] = "Post added to favorites."
            return Response(data, status=status.HTTP_201_CREATED)