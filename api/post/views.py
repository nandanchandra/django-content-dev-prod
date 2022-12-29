import logging
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from api.post.filters import PostFilter
from api.post.models import Post
from api.post.serializers import PostCreateSerializer, PostSerializer, PostUpdateSerializer
from api.utils.custom_view_exceptions import UpdatePost
from api.utils.pagination import DefaultPagination
from api.utils.permission import IsOwnerOrReadOnly
from api.utils.renderers import CustomeJSONRenderer

User = get_user_model()
logger = logging.getLogger(__name__)

class PostCreateAPIView(generics.CreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostCreateSerializer
    renderer_classes = [CustomeJSONRenderer]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data,context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"post {serializer.data.get('title')} created")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Post.objects.all()
    renderer_classes = [CustomeJSONRenderer,]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilter

@api_view(["PATCH","PUT"])
@permission_classes([permissions.IsAuthenticated])
def updatePostApiView(request,id):
    try:
        post = Post.objects.get(pkid=id)
    except Post.DoesNotExist:
        raise NotFound("That Post does not exist in our catalog")
    user = request.user
    if post.author != user:
        raise UpdatePost
    data = request.data
    serializer = PostUpdateSerializer(post,data=data,many=False)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    except:
        return Response(serializer.errors)

class PostDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    lookup_field = "pkid"

    def delete(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pkid=self.kwargs.get("pkid"))
            self.destroy(request)
            return Response("Post was successful deleted")
        except Post.DoesNotExist:
            logger.info(f"Error Occured: {Post}")
            raise NotFound("That Post does not exist in our catalog")
        except Exception as e:
            logger.info(f"Error Occured: {e}")
            return Response("Error occur while deleting post")