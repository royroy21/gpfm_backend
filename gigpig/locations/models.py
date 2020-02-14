from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.postgres.fields import JSONField
from django.db import models

from gigpig.core.models import DateCreatedUpdatedMixin


class Country(DateCreatedUpdatedMixin):
    name = models.CharField(max_length=254, unique=True)
    code = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Location(DateCreatedUpdatedMixin):
    name = models.CharField(max_length=254)
    description = models.TextField(default="", blank=True)

    # TODO - check if these fields (see link) are better suited ...
    # https://docs.djangoproject.com/en/3.0/ref/contrib/gis/model-api/
    # northeast_bounds = geo_models.PointField()
    # southwest_bounds = geo_models.PointField()

    geometry = geo_models.PointField()
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="locations",
    )
    TYPE_VILLAGE = "village"
    TYPE_NEIGHBOURHOOD = "neighbourhood"
    TYPE_CITY = "city"
    TYPE_COUNTY = "county"
    TYPE_POSTCODE = "postcode"
    TYPE_TERMINATED_POSTCODE = "terminated_postcode"
    TYPE_STATE_DISTRICT = "state_district"
    TYPE_STATE = "state"
    TYPE_REGION = "region"
    TYPE_ISLAND = "island"
    TYPE_COUNTRY = "country"
    TYPE_UNKNOWN = "unknown"
    TYPES = [
        (TYPE_VILLAGE, "Village"),
        (TYPE_NEIGHBOURHOOD, "Neighbourhood"),
        (TYPE_CITY, "City"),
        (TYPE_COUNTY, "County"),
        (TYPE_POSTCODE, "Postcode"),
        (TYPE_TERMINATED_POSTCODE, "Terminated Postcode"),
        (TYPE_STATE_DISTRICT, "State District"),
        (TYPE_STATE, "State"),
        (TYPE_REGION, "Region"),
        (TYPE_ISLAND, "Island"),
        (TYPE_COUNTRY, "Country"),
        (TYPE_UNKNOWN, "Unknown"),
    ]
    type = models.CharField(
        max_length=254,
        choices=TYPES,
        default=TYPE_UNKNOWN,
    )
    components = JSONField(default=dict)

    def __str__(self):
        return "{} ({})".format(self.name, self.country.code)

    @classmethod
    def get_nearest_locations(cls, miles, latitude, longitude):
        point = GEOSGeometry(
            'POINT({} {})'.format(longitude, latitude),
            srid=settings.SRID,
        )
        return Location.objects.filter(
            geometry__distance_lte=(point, D(mi=miles)))

    def get_nearest_locations_to_this(self, miles):
        longitude, latitude = self.geometry.coords
        return self.get_nearest_locations(miles, latitude, longitude)
