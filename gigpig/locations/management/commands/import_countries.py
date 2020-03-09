import csv
from django.core.management.base import BaseCommand
from gigpig.locations import models


class Command(BaseCommand):
    COUNTRIES_FILE = "/code/gigpig/locations/country_codes.csv"
    help = 'Creates countries from {}'.format(COUNTRIES_FILE)

    def handle(self, *args, **options):
        with open(self.COUNTRIES_FILE) as f:
            countries = [
                models.Country(**{
                    "name": name,
                    "code": code,
                })
                for name, code in csv.reader(f)
            ]
            self.stdout.write(self.style.SUCCESS(
                f"creating {len(countries)} new countries"
            ))
            models.Country.objects.bulk_create(countries)
            self.stdout.write(self.style.SUCCESS("finished"))
