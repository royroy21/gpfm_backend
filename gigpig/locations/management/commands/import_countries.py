from django.core.management.base import BaseCommand

from gigpig.locations import models


class Command(BaseCommand):
    COUNTRIES_FILE = "/code/gigpig/locations/country_codes.csv"
    help = 'Creates countries from {}'.format(COUNTRIES_FILE)

    def handle(self, *args, **options):
        with open(self.COUNTRIES_FILE) as f:
            countries = [
                models.Country(**self.get_country_name_and_code(country_data))
                for country_data
                in f.readlines()
            ]
            self.stdout.write(self.style.SUCCESS(
                f"creating {len(countries)} new countries"
            ))
            models.Country.objects.bulk_create(countries)
            self.stdout.write(self.style.SUCCESS("finished"))

    def get_country_name_and_code(self, country_data):
        name, code = country_data.split(",")
        return {
            "name": name,
            "code": code.rstrip("\n"),
        }
