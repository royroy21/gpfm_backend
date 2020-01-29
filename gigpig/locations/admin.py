from django.contrib import admin

from gigpig.locations import models


class CountryAdmin(admin.ModelAdmin):
    ordering = (
        "code",
    )
    search_fields = (
        "code",
    )


class LocationAdmin(admin.ModelAdmin):
    ordering = (
        "name",
    )
    search_fields = (
        "name",
    )


admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Location, LocationAdmin)
