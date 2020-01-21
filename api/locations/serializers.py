from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from locations import documents, services


class LocationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.LocationDocument
        fields = (
            'id',
            'name',
            'description',
        )


class BaseGeocodingSerializer(serializers.Serializer):

    service = None

    def resolve_query(self, *args, **kwargs):
        raise NotImplemented

    def create(self, validated_data):
        raise ValidationError("Cannot create")

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")


class ForwardGeocodingSerializer(BaseGeocodingSerializer):

    geocoding_service = services.ForwardGeocodingOpenCageAPI()

    def resolve_query(self, query, country):
        if not query or not country:
            raise ValidationError("Missing parameters. "
                                  "'q' and 'country' required")

        return self.geocoding_service.resolve_query(query, country)


class ReverseGeocodingSerializer(BaseGeocodingSerializer):

    geocoding_service = services.ReverseGeocodingOpenCageAPI()

    def resolve_query(self, latitude, longitude):
        if not latitude or not longitude:
            raise ValidationError("Missing parameters. 'latitude'"
                                  " and 'longitude' required")

        return self.geocoding_service.resolve_query(latitude, longitude)
