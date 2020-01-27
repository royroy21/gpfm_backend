from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.locations import serializers
from api.pagination import CustomPageNumberPagination
from locations.documents import LocationDocument
from api.locations.serializers import LocationDocumentSerializer


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

    # TODO - set auth
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    forward_geocoding_serializer = serializers.ForwardGeocodingSerializer
    reverse_geocoding_serializer = serializers.ReverseGeocodingSerializer

    @action(methods=['get'], detail=False, url_path='forward-geocoding')
    def forward_geocoding(self, request):
        country = request.query_params.dict().get("country")
        query = self.request.query_params.dict().get("q")
        results = self.forward_geocoding_serializer()\
            .resolve_query(query, country)
        return Response(results)

    # TODO - consider removing this. I don't think it's needed
    # @action(methods=['get'], detail=False, url_path='reverse-geocoding')
    # def reverse_geocoding(self, request):
    #     latitude = request.query_params.dict().get("latitude")
    #     longitude = self.request.query_params.dict().get("longitude")
    #     results = self.reverse_geocoding_serializer()\
    #         .resolve_query(latitude, longitude)
    #     return Response(results)
