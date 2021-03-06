from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from gigpig.api.locations import serializers
from gigpig.api.pagination import CustomPageNumberPagination
from gigpig.locations.documents import LocationDocument
from gigpig.api.locations.serializers import LocationDocumentSerializer
from gigpig.locations import models


class CountryViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.order_by("name")


class LocationViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.order_by("-title")


# TODO - requires auth
# TODO - do we need this api to be functioning?
class LocationsSearchViewSet(DocumentViewSet):
    document = LocationDocument
    serializer_class = LocationDocumentSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    filter_backends = [
        CompoundSearchFilterBackend,
    ]

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


class LocationsGeocodingViewSet(viewsets.ViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    forward_geocoding_serializer = serializers.ForwardGeocodingSerializer
    reverse_geocoding_serializer = serializers.ReverseGeocodingSerializer

    @action(methods=['get'], detail=False, url_path='forward-query')
    def forward_geocoding(self, request):
        country = request.query_params.dict().get("country")
        query = self.request.query_params.dict().get("q")
        results = self.forward_geocoding_serializer()\
            .resolve_query(query, country)
        return Response(results)

    # TODO - consider removing this. I don't think it's needed
    # @action(methods=['get'], detail=False, url_path='reverse-query')
    # def reverse_geocoding(self, request):
    #     latitude = request.query_params.dict().get("latitude")
    #     longitude = self.request.query_params.dict().get("longitude")
    #     results = self.reverse_geocoding_serializer()\
    #         .resolve_query(latitude, longitude)
    #     return Response(results)
