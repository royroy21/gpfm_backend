# Generated by Django 2.2.2 on 2019-08-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genres', '0001_initial'),
        ('users', '0005_user_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='genres',
            field=models.ManyToManyField(related_name='users', to='genres.Genre'),
        ),
    ]
