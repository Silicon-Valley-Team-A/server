from django.db import models
from account.models import *


class Playlist(models.Model):
    user = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'playlist'


class Song(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=200, blank=True, null=True)
    artist = models.CharField(max_length=50, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    file = models.CharField(max_length=500, blank=True, null=True)
    title_album = models.CharField(max_length=200, blank=True, null=True)
    image_album = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'song'


class Songlist(models.Model):
    playlist = models.ForeignKey(Playlist, models.DO_NOTHING, blank=True, null=True)
    song = models.ForeignKey(Song, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'songlist'