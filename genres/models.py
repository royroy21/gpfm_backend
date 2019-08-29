from django.db import models

from core.models import DateCreatedUpdatedMixin


class Genre(DateCreatedUpdatedMixin):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name
