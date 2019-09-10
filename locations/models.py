from django.contrib.gis.geos import Point
from django.db import models

from core.models import DateCreatedUpdatedMixin


class Country(DateCreatedUpdatedMixin):
    code = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.code


class Location(DateCreatedUpdatedMixin):
    name = models.CharField(max_length=254, unique=True)
    geometry = Point()
    country = models.ForeignKey(
        "locations.Country",
        on_delete=models.CASCADE,
        related_name="locations",
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.country.code)
