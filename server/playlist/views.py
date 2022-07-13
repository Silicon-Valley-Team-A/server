from genericpath import exists
from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.core import serializers
from .models import *
import json
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['POST'])
def save(request):
    data = request.data

    new_playlist = Playlist.objects.create(
        user_id=data['user_id'],
        name=data['name'],
        tag=data['tag']
    )
    new_playlist.save()

    if 'songs' in data:
        for s in data['songs']:
            song_obj = Song.objects.create(id=s['id'],
                                           title=s['title'],
                                           artist=s['artist'],
                                           duration=s['duration'],
                                           file=s['file'],
                                           title_album=s['title_album'],
                                           image_album=s['image_album'])
            Song.save(song_obj)

            songlist_obj = Songlist.objects.create(
                playlist_id=3,
                song_id=s['id']
            )
            Songlist.save(songlist_obj)

    return Response("success")


@api_view(['POST'])
def show(request):
    data = request.data
    songlist = Songlist.objects.filter(playlist_id=data['playlist_id'])
    songs = []

    for songlist in songlist:
        song = Song.objects.filter(id=songlist.song_id)
        songs += song
    songs = serializers.serialize("json", songs)
    songs = json.loads(songs)
    return Response(songs)
