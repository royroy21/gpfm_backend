from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from locations import documents


class LocationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.LocationDocument
        fields = (
            'id',
            'name',
            'description',
        )
