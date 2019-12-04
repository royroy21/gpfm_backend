import datetime

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from locations import models


class Command(BaseCommand):
    COUNTRIES_FILE = "/code/locations/gb.txt"
    help = 'Creates Countries and Locations from {}'.format(COUNTRIES_FILE)

    # http://www.geonames.org/export/codes.html
    POPULATED_LOCATION_CODES = [
        "PPL",
        "PPLA",
        "PPLA2",
        "PPLA3",
        "PPLA4",
        "PPLA5",
        "PPLC",
        "PPLCH",
        "PPLF",
        "PPLG",
        "PPLH",
        "PPLL",
        "PPLQ",
        "PPLR",
        "PPLS",
        "PPLW",
        "PPLX",
    ]

    def handle(self, *args, **options):
        counter = 1
        start = datetime.datetime.now()
        for line in open(self.COUNTRIES_FILE):
            parsed_line = line.split("\t")

            location_code = parsed_line[7]
            if location_code not in self.POPULATED_LOCATION_CODES:
                continue

            name = parsed_line[1]
            country, _ = \
                models.Country.objects.get_or_create(code=parsed_line[8])
            coords = (
                float(parsed_line[5]),
                float(parsed_line[4]),
            )
            point = Point(coords)

            message = "{}] {}, ({}) {}".format(
                counter,
                name,
                country.code,
                point.coords,
            )
            if models.Location.objects\
                    .filter(name=name, country=country).exists():
                self.stdout.write(self.style.WARNING("[skipping " + message))
            else:
                models.Location.objects.create(
                    name=name,
                    country=country,
                    geometry=point,
                )
                self.stdout.write(self.style.SUCCESS("[processed " + message))

            counter += 1

        time = datetime.datetime.now() - start
        self.stdout.write(self.style.SUCCESS(
            "[finish] completed in {} seconds".format(time.total_seconds()),
        ))
