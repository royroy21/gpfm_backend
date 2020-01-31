from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from gigpig.locations import models


@registry.register_document
class LocationDocument(Document):
    id = fields.IntegerField(attr='id')
    description = fields.StringField(
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )
    name = fields.StringField(
        fields={
            'raw': fields.StringField(analyzer='keyword'),
        }
    )

    class Django:
        model = models.Location

    class Index:
        name = "locations"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
