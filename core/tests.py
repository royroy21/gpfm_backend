from os import listdir
from unittest import TestCase

from django.conf import settings


class TestMigrations(TestCase):

    def test_migrations_are_named(self):
        migrations_not_named = []

        for local_app in settings.LOCAL_APPS:
            migrations_directory = "{}/migrations".format(local_app)
            for migration_file in listdir(migrations_directory):
                if "_auto_" in migration_file:
                    migrations_not_named.append("{}/{}".format(
                        migrations_directory, migration_file))

        self.assertEqual(migrations_not_named, [])
