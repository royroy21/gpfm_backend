from django_dynamic_fixture import G
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from genres.models import Genre
from users.models import User


class TestListGenres(TestCase):

    endpoint = reverse("list_genres")

    def setUp(self):
        email = "roy@example.com"
        user = G(User, email=email)

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        G(Genre, name="electronic")
        G(Genre, name="indie")

    def test_list_genres_with_valid_user(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 2)
        for genreData in response_json:
            self.assertTrue(Genre.objects.filter(**genreData).exists())

    def test_delete_genre(self):
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, 405)

    def test_list_genres_with_invalid_user(self):
        response = APIClient().get(self.endpoint)
        self.assertEqual(response.status_code, 401)
