from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from gigpig.genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
        )
        read_only_fields = fields

    def create(self, validated_data):
        raise ValidationError("Cannot create")

    def update(self, instance, validated_data):
        raise ValidationError("Cannot update")
