from rest_framework import serializers
from api.services.models import Rating,Comment,Favorite

class RatingSerializer(serializers.ModelSerializer):
    rated_by = serializers.SerializerMethodField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "post", "rated_by", "value"]

    def get_rated_by(self, obj):
        return obj.rated_by.username

    def get_post(self, obj):
        return obj.post.title

class PostCommentSerializer(serializers.ModelSerializer):
    
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "body", "created_at", "updated_at"]

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "user", "post"]