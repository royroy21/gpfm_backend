from django.contrib import admin

from genres.models import Genre


class GenreAdmin(admin.ModelAdmin):
    ordering = (
        "name",
    )
    search_fields = (
        "name",
    )


admin.site.register(Genre, GenreAdmin)
