from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db import models

from core.models import DateCreatedUpdatedMixin


class Country(DateCreatedUpdatedMixin):
    code = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.code


class Location(DateCreatedUpdatedMixin):
    name = models.CharField(max_length=254)
    description = models.TextField(default="", blank=True)
    geometry = geo_models.PointField()
    country = models.ForeignKey(
        "locations.Country",
        on_delete=models.CASCADE,
        related_name="locations",
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.country.code)

    @classmethod
    def get_nearest_locations(cls, miles, latitude, longitude):
        # TODO - investigate what is srid
        point = \
            GEOSGeometry('POINT({} {})'.format(longitude, latitude), srid=4326)
        return Location.objects.filter(
            geometry__distance_lte=(point, D(mi=miles)))

    def get_nearest_locations_to_this(self, miles):
        longitude, latitude = self.geometry.coords
        return self.get_nearest_locations(miles, latitude, longitude)
