import logging
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from api.post.serializers import PostCreateSerializer
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