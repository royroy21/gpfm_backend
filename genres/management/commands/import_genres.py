from django.core.management.base import BaseCommand

from genres import models


class Command(BaseCommand):
    GENRES_FILE = "/code/genres/genres.txt"
    help = 'Creates genres from {}'.format(GENRES_FILE)

    def handle(self, *args, **options):
        genres = self.get_genres()
        self.stdout.write(self.style.SUCCESS(
            "creating {} new genres".format(len(genres))
        ))
        models.Genre.objects.bulk_create(genres)
        self.stdout.write(self.style.SUCCESS("finished"))

    def get_genres(self):
        existing_genres = \
            models.Genre.objects.values_list("name", flat=True)
        with open(self.GENRES_FILE) as file:
            file_contents = file.readlines()
            new_genres = [
                models.Genre(name=self.clean_genre(genre))
                for genre
                in file_contents
                if self.clean_genre(genre) not in existing_genres
            ]
        return new_genres

    def clean_genre(self, genre):
        return genre.strip().lower()
