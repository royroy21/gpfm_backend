from django.contrib import admin

from gigpig.gigs import models


class GigAdmin(admin.ModelAdmin):
    ordering = (
        "title",
    )
    search_fields = (
        "title",
    )


admin.site.register(models.Gig, GigAdmin)
