from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as \
    DjoserUserCreateSerializer
from rest_framework.serializers import CharField


User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    pass


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
        )

    def validate(self, attrs):
        re_password = attrs.pop('re_password')
        attrs = super().validate(attrs)
        if attrs['password'] == re_password:
            return attrs
        else:
            self.fail('password_mismatch')
