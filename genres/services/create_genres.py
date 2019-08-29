from genres.models import Genre


class CreateGenres:

    filename = "genres/services/genres.txt"

    def create_genres(self):
        return Genre.objects.bulk_create(self.get_genres())

    def get_genres(self):
        genres = Genre.objects.values_list("name", flat=True)
        return [
            Genre(name=self.clean_genre(genre))
            for genre
            in open(self.filename)
            if self.clean_genre(genre) not in genres
        ]

    def clean_genre(self, genre):
        return genre.strip().lower()
