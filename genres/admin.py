from django.contrib import admin

from genres.models import Genre


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)
