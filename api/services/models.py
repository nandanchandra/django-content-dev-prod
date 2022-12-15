from django.db import models
from django.contrib.auth import get_user_model
from api.post.models import Post
from api.utils.models import TimeStampedUUIDModel
from api.utils.preferences import RATING,REACTION
User = get_user_model()

class Rating(TimeStampedUUIDModel):

    post = models.ForeignKey(Post, related_name="post_ratings", on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User, related_name="user_who_rated", on_delete=models.CASCADE)
    value = models.IntegerField(choices=RATING,default=0,help_text="1=POOR, 2=FAIR, 3=AVERAGE, 4=GOOD, 5=BEST",)
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ["rated_by", "post"]

    def __str__(self):
        return f"{self.post.title} rated at {self.value}"

class Comment(TimeStampedUUIDModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"{self.author} commented on {self.post}"

class Favorite(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_favorites")

    def __str__(self):
        return f"{self.user.username} favorited {self.post.title}"

    def is_favorited(self, user, post):
        _result=False
        try:
            post = self.post
            user = self.user
        except Post.DoesNotExist:
            pass
        finally:
            queryset = Favorite.objects.filter(post_id=post, user_id=user)
        if queryset:
            _result=True
        return _result

class ReactionManager(models.Manager):

    def likes(self):
        return self.get_queryset().filter(reaction__gt=0).count()
    def dislikes(self):
        return self.get_queryset().filter(reaction__lt=0).count()
    def has_reacted(self):
        request = self.context.get("request")
        if request:
            self.get_queryset().filter(user=request)

class Reaction(TimeStampedUUIDModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reactions")
    reaction = models.IntegerField(choices=REACTION)

    objects = ReactionManager()

    class Meta:
        unique_together = ["user", "post", "reaction"]

    def __str__(self):
        return (f"{self.user.username} voted on {self.post.title} with a {self.reaction}")