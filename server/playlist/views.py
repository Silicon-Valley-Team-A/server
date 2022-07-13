from msilib.schema import Error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import *
import json
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
import requests

# Create your views here.

#@api_view(['POST'])
def save(request):
    if request.method =="POST":
    #data = request.data
        new_playlist = Playlist.objects.create(
            user_id=request.POST['user_id'],
            name=request.POST['name'],
            tag=request.POST['tag']
        )
        new_playlist.save()
        maxid=Playlist.objects.aggregate(Max('id'))
        #new_playlist.id

        if 'songs' in request.POST:
            for s in request.POST['songs']:
                song_obj = Song.objects.create(id=s['id'],
                                        title=s['title'],
                                        artist=s['artist'],
                                        duration=s['duration'],
                                        file=s['file'],
                                        title_album=s['title_album'],
                                        image_album=s['image_album'])
                Song.save(song_obj)

                songlist_obj = Songlist.objects.create(
                    playlist_id=maxid['id__max'],
                    song_id=s['id']
                )
                Songlist.save(songlist_obj)

        return requests.post(url)
