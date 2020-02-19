import logging

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from gigpig.api.fields import GeometryField
from gigpig.locations import documents, models, services

logger = logging.getLogger(__name__)


class LocationSerializer(serializers.ModelSerializer):

    geometry = GeometryField()

    class Meta:
        model = models.Location
        fields = (
            "country",
            "description",
            "geometry",
            "id",
            "name",
            "type",
        )


class LocationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.LocationDocument
        fields = (
            'id',
            'name',
            'description',
        )


class BaseGeocodingSerializer(serializers.Serializer):

    cache_service = None
    geocoding_service = None

    parser = services.OpenCageParser

    def resolve_query(self, *args, **kwargs):
        raise NotImplemented

    def create(self, validated_data):
        raise ValidationError("Cannot create")

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")


class ForwardGeocodingSerializer(BaseGeocodingSerializer):

    cache_service = services.ForwardGeocodingCache
    geocoding_service = services.ForwardGeocodingOpenCageAPI

    def resolve_query(self, query, country):
        if not query or not country:
            raise ValidationError("Missing parameters. "
                                  "'q' and 'country' required")

        cache = self.cache_service()
        cached_response = cache.get(query, country)
        if cached_response:
            logger.debug("Returning forward geocoding response from cache. "
                         "Values: %s %s", query, country)
            return cached_response

        response = self.geocoding_service().resolve_query(query, country)
        if not response:
            logger.warning("Nothing returned for forward geocoding "
                           "response from api. Values: %s %s", query, country)
            return []

        logger.debug("Returning forward geocoding response from api. "
                     "Values: %s %s", query, country)
        parse_results = self.parser().parse_results(response, query)
        cache.set(query, country, parse_results)
        return parse_results


class ReverseGeocodingSerializer(BaseGeocodingSerializer):

    cache_service = services.ReverseGeocodingCache
    geocoding_service = services.ReverseGeocodingOpenCageAPI

    def resolve_query(self, latitude, longitude):
        if not latitude or not longitude:
            raise ValidationError("Missing parameters. 'latitude'"
                                  " and 'longitude' required")

        cache = self.cache_service()
        cached_response = cache.get(latitude, longitude)
        if cached_response:
            logger.debug(
                "Returning reverse geocoding response from cache. "
                "Values: %s %s", latitude, longitude)
            return cached_response

        response = self.geocoding_service().resolve_query(latitude, longitude)
        if not response:
            logger.warning("Nothing returned for reverse geocoding response "
                           "from api. Values: %s %s", latitude, longitude)
            return []

        logger.debug("Returning reverse geocoding response from api. "
                     "Values: %s %s", latitude, longitude)
        parse_results = self.parser().parse_results(response)
        cache.set(latitude, longitude, parse_results)
        return parse_results
