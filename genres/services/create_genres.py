from genres.models import Genre


class CreateGenres:

    filename = "genres/services/genres.txt"

    def create_genres(self):
        return Genre.objects.bulk_create(self.get_genres())

    def get_genres(self):
        existing_genres = Genre.objects.values_list("name", flat=True)
        with open(self.filename) as file:
            file_contents = file.readlines()
            new_genres = [
                Genre(name=self.clean_genre(genre))
                for genre
                in file_contents
                if self.clean_genre(genre) not in existing_genres
            ]
        return new_genres

    def clean_genre(self, genre):
        return genre.strip().lower()
