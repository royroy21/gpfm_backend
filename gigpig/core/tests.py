from os import listdir
from unittest import TestCase

from django.conf import settings


class TestMigrations(TestCase):

    def test_migrations_are_named(self):
        migrations_not_named = []

        for local_app in settings.LOCAL_APPS:
            local_app_path = "/".join(local_app.split("."))
            migrations_directory = "{}/migrations".format(local_app_path)
            migrations_not_named.extend([
                "{}/{}".format(migrations_directory, migration_file)
                for migration_file in listdir(migrations_directory)
                if "_auto_" in migration_file
            ])

        self.assertEqual(migrations_not_named, [])
