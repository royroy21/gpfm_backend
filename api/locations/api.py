from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
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
    ]

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )
