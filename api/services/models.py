from django.db import models
from django.contrib.auth import get_user_model
from api.post.models import Post
from api.utils.models import TimeStampedUUIDModel
from api.utils.preferences import RATING
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
