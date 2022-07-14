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
from django.db.models import Max
import requests

# Create your views here.

# @api_view(['POST'])


def save(request):
    if request.method == "POST":
        #data = request.data
        new_playlist = Playlist.objects.create(
            user_id=request.POST['user_id'],
            name=request.POST['name'],
            tag=request.POST['tag']
        )
        new_playlist.save()
        maxid = Playlist.objects.aggregate(Max('id'))
        # maxid=new_playlist.id

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
            data={
                "status":"success",  
                "message":"songs data saved"
                }
            return HttpResponse(data, content_type="application/json")

        else:
            data={
                "status":"error",
                "message":"no songs data"
                }
            return HttpResponse(data, content_type="application/json")


# @api_view(['POST'])
def show(request):
    #data = request.data
    if request.method == "POST":
        songlist = Songlist.objects.filter(
            playlist_id=request.POST['playlist_id'])
        songs = []

        for songlist in songlist:
            song = Song.objects.filter(id=songlist.song_id)
            songs += song
        songs = serializers.serialize("json", songs)
        songs = json.loads(songs)
        return Response(songs)
