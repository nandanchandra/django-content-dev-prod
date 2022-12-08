from django.db import models
from django.contrib.auth import get_user_model
from api.utils.models import TimeStampedUUIDModel

User = get_user_model()
class Tag(TimeStampedUUIDModel):
    tag = models.CharField(max_length=80)
    class Meta:
        ordering = ["tag"]

    def __str__(self):
        return self.tag

class Post(TimeStampedUUIDModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    body = models.TextField()
    post_image = models.ImageField(blank=True,null=True)
    tags = models.ManyToManyField(Tag,related_name="posts")
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}'s post"

    @property
    def list_of_tags(self):
        tags = [tag.tag for tag in self.tags.all()]
        return tags

class PostViews(TimeStampedUUIDModel):
    ip = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name="post_views", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Total views on - {self.post.title} is - {self.post.views} view(s)")
    class Meta:
        verbose_name = "Total views on post"
        verbose_name_plural = "Total post Views"