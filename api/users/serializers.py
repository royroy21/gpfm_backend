from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as \
    DjoserUserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import CharField

from api.genres.serializers import GenreSerializer
from genres.models import Genre


User = get_user_model()


class CurrentUserSerializer(DjoserUserSerializer):
    avatar = serializers.ImageField(
        allow_empty_file=True,
        allow_null=True,
        required=False,
    )
    genres = GenreSerializer(many=True)

    class Meta:
        model = User
        simple_update_fields = (
            "bio",
            "dob",
            "handle",
        )
        fields = tuple(User.REQUIRED_FIELDS) + simple_update_fields + (
            settings.LOGIN_FIELD,
            "avatar",
            "genres",
            "id",
        )
        read_only_fields = (
            settings.LOGIN_FIELD,
            "id",
        )

    def update(self, instance, validated_data):
        self.update_genres(instance)

        for field in self.Meta.simple_update_fields:
            data = validated_data.get(field)
            if data is not None:
                setattr(instance, field, data)

        # We want None value to delete avatar
        if "avatar" in validated_data:
            instance.avatar = validated_data.get("avatar")

        instance.save()
        return instance

    def update_genres(self, instance):
        genres = self.initial_data.get("genres", [])

        for genreData in genres:
            genre = Genre.objects.filter(**genreData).last()
            if genre:
                instance.genres.add(genre)


class CreatePasswordRetypeSerializer(DjoserUserCreateSerializer):

    re_password = CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    default_error_messages = {
        'password_mismatch': _('Password fields do not match.'),
    }

    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            "password",
            "re_password",
            "handle",
        )

    def validate(self, attrs):
        re_password = attrs.pop('re_password')
        attrs = super().validate(attrs)
        if attrs['password'] != re_password:
            self.fail('password_mismatch')
        return attrs

