# Generated by Django 4.0.5 on 2022-07-11 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
        migrations.DeleteModel(
            name='Songlist',
        ),
    ]
