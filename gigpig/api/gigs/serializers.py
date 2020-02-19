from rest_framework import serializers

from gigpig.gigs import models


class GigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gig
        fields = (
            "id",
            "title",
            "venue",
            "location",
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
