from django.test import TestCase
from django_dynamic_fixture import G

from gigpig.api.locations import serializers
from gigpig.locations import models


class TestLocationSerializer(TestCase):

    serializer = serializers.LocationSerializer

    def setUp(self):
        self.country = G(models.Country, name="Great Britain", code="GB")
        self.default_data = {
            "country": self.country.id,
            "geometry": [
                51.4826053,
                0.0365359,
            ],
            "name": "Charlton, Royal Borough of Greenwich",
            "type": "neighbourhood",
            "components": {
                "city": "London",
            },
        }

    def create_location(self):
        serializer = self.serializer(data=self.default_data)
        self.assertTrue(serializer.is_valid())
        return serializer.save()

    def test_create_location(self):
        self.create_location()

        locations = \
            models.Location.objects.filter(name=self.default_data["name"])
        self.assertTrue(locations.exists())

    def test_create_existing_location(self):
        self.create_location()
        second_location = self.create_location()
        locations = \
            models.Location.objects.filter(name=self.default_data["name"])

        self.assertEqual(locations.count(), 1)
        self.assertEqual(second_location.id, locations.first().id)
