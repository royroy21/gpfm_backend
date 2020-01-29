from django_dynamic_fixture import G
from django.test import TestCase

from gigpig.api.users import serializers
from gigpig.genres.models import Genre
from gigpig.users import models


class TestCurrentUserSerializer(TestCase):

    serializer = serializers.CurrentUserSerializer

    def setUp(self):
        self.user = G(models.User)

    def test_update_genres(self):
        genre_electronic = G(Genre, name="electronic")
        genres_indie = G(Genre, name="indie")
        data = {
            "genres": [genre_electronic.id, genres_indie.id],
        }
        serializer = \
            self.serializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertIn(genre_electronic, user.genres.all())
        self.assertIn(genres_indie, user.genres.all())

    def test_update_bio(self):
        expected_bio = "Hey!"
        data = {
            "bio": expected_bio,
        }
        serializer = \
            self.serializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.bio, expected_bio)
