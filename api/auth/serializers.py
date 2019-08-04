from djoser.serializers import TokenCreateSerializer as \
    DjoserTokenCreateSerializer
from rest_framework.validators import ValidationError


class TokenCreateSerializer(DjoserTokenCreateSerializer):

    def validate(self, attrs):
        return super().validate(self.get_attrs_with_lowercase_email(attrs))

    def get_attrs_with_lowercase_email(self, attrs):
        email = attrs.get("email")

        if isinstance(email, str):
            email = email.lower()
        return {
            **attrs,
            "email": email,
        }

    def create(self, validated_data):
        raise ValidationError("Create method disabled.")

    def update(self, instance, validated_data):
        raise ValidationError("Update method disabled.")
