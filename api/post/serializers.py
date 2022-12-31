from rest_framework import serializers
from api.post.models import Post
from api.account.models import User
from api.post.field_utils import TagRelatedField

class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=serializers.CurrentUserDefault(),required=False)
    tags = TagRelatedField(many=True,required=False)
    post_image = serializers.ImageField()

    class Meta:
        model = Post
        exclude = ["updated_at","pkid"]

class PostSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField(read_only=True)
    post_image = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField(source="post_read_time")
    ratings = serializers.SerializerMethodField()
    num_ratings = serializers.SerializerMethodField()
    tagList = TagRelatedField(many=True, required=False, source="tags")
    comments = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id","title","tagList","description","body","post_image","read_time","author_info","likes","dislikes","ratings","num_ratings","average_rating","views","num_comments","comments","created_at","updated_at"]

class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    title=serializers.CharField(required=False)
    description=serializers.CharField(required=False)
    body=serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ["title", "description", "body", "post_image", "tags"]