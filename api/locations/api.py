from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_GEO_DISTANCE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    GeoSpatialFilteringFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from api.pagination import CustomPageNumberPagination
from locations.documents import LocationDocument
from api.locations.serializers import LocationDocumentSerializer


class LocationSearchViewSet(DocumentViewSet):
    document = LocationDocument
    serializer_class = LocationDocumentSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = 'id'

    filter_backends = [
        CompoundSearchFilterBackend,
        GeoSpatialFilteringFilterBackend,
    ]

    geo_spatial_filter_fields = {
        'location': {
            'lookups': [
                LOOKUP_FILTER_GEO_DISTANCE,
            ],
        },
    }

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )
