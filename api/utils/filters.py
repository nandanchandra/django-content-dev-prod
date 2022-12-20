import django_filters as filters
from api.post.models import Post

class PostFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author__first_name", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags", method="get_post_tags", lookup_expr="iexact")
    created_at = filters.IsoDateTimeFilter(field_name="created_at")
    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    class Meta:
        model = Post
        fields = ["author", "title", "tags", "created_at", "updated_at"]

    def get_post_tags(self, queryset, tags, value):
        tag_values = value.replace(" ", "").split(",")
        return queryset.filter(tags__tag__in=tag_values).distinct()