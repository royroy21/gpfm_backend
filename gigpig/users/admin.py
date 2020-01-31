from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from gigpig.users.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
            'handle',
            'bio',
            'dob',
            'genres',
            'avatar',
            'password',
            'last_login',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            # 'groups',
            # 'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'handle',
                'password1',
                'password2',
            ),
        }),
    )

    list_display = (
        'email',
        'handle',
        'is_staff',
        'last_login',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    search_fields = (
        'email',
        'handle',
    )
    ordering = (
        'email',
    )
    # filter_horizontal = (
    #     'groups',
    #     'user_permissions',
    # )
    readonly_fields = (
    )


admin.site.register(User, UserAdmin)
