from rest_framework import serializers
from api.post.models import Tag

class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()
    def to_internal_value(self, data):
        tag,created= Tag.objects.get_or_create(tag=data)
        return tag
    def to_representation(self, value):
        return value.tag
