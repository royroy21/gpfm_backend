from djoser.serializers import TokenCreateSerializer


class CustomTokenCreateSerializer(TokenCreateSerializer):

    # TODO - not totally convinced this is the best place for this
    def validate(self, attrs):
        attrs_copy = attrs.copy()

        if "email" in attrs_copy:
            email = attrs_copy["email"]
            if isinstance(email, str):
                attrs_copy["email"] = attrs_copy["email"].lower()

        return super().validate(attrs_copy)
