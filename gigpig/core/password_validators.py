from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NoSpacesPasswordValidator:

    def validate(self, password, user=None):
        if isinstance(password, str):
            if " " in password:
                raise ValidationError(
                    _("Password must not contain spaces."),
                )

    def get_help_text(self):
        return _("Password must not contain spaces.")
