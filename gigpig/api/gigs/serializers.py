from rest_framework import serializers

from gigpig.gigs import models


class GigSerializer(serializers.ModelSerializer):

    location_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Gig
        fields = (
            "id",
            "title",
            "venue",
            "location",
            "location_name",
            "date_created",
            "description",
            "genres",
            "image",
            "start_date",
            "end_date",
            "user",
        )
        read_only_fields = (
            "id",
        )

    def get_location_name(self, obj):
        return obj.location.name
