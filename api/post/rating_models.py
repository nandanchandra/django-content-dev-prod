from django.db import models
from django.contrib.auth import get_user_model
from api.utils.models import TimeStampedUUIDModel
User = get_user_model()

class Rating(TimeStampedUUIDModel):

    post = models.ForeignKey("posts.Post", related_name="post_ratings", on_delete=models.CASCADE)
    rated_by = models.ForeignKey(User, related_name="user_who_rated", on_delete=models.CASCADE)
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ["rated_by", "post"]

    def __str__(self):
        return f"{self.post.title} rated at {self.value}"
