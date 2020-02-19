from django.db import models

from gigpig.core.models import DateCreatedUpdatedMixin


class Gig(DateCreatedUpdatedMixin):
    title = models.CharField(max_length=254, unique=True)
    venue = models.CharField(max_length=254, unique=True)
    location = \
        models.ForeignKey("locations.Location", on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True)
    genres = models.ManyToManyField("genres.Genre")
    image = models.ImageField(upload_to="images", blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.user.get_username()}"
