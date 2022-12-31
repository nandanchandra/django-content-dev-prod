from rest_framework import serializers
from api.services.models import Rating

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