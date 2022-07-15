from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from account.models import *
from .models import *
import json
from rest_framework.response import Response

# Create your views here.
@method_decorator(csrf_exempt)
def save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id=data.get('user_id')
        if User.objects.filter(id=user_id).exists():
            user_data = User.objects.get(id=user_id)
        else:
            return JsonResponse({"status":"error", "message":"You need to login first", "user_id":user_id})            

        new_playlist = Playlist.objects.create(
            user=user_data,
            name=data.get('name'),
            tag=data.get('tag')
        )
        new_playlist.save()

        if 'songs' in data:
            for s in data.get('songs'):
                song_obj = Song.objects.create(id=s['id'],
                                               title=s['title'],
                                               artist=s['artist'],
                                               duration=s['duration'],
                                               file=s['file'],
                                               title_album=s['title_album'],
                                               image_album=s['image_album'])
                Song.save(song_obj)

                songlist_obj = Songlist.objects.create(
                    playlist_id=new_playlist.id,
                    song_id=s['id']
                )
                Songlist.save(songlist_obj)
            return JsonResponse({"status":"success", "message":"successfully saved"})
        else:
            return JsonResponse({"status":"error", "message":"no songs data"})
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})

def playlist(request):
    if request.method == "GET":
        data = json.loads(request.body)
        user_id=data.get('user_id')
        if User.objects.filter(id=user_id).exists():
            playlists = Playlist.objects.filter(user=User.objects.filter(id=user_id))
        else:
            return JsonResponse({"status":"error", "message":"You need to login first", "user_id":user_id}) 

        playlists = serializers.serialize("json", playlists)
        playlists = json.loads(playlists)
        return Response(playlists)
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})

def showplaylist(request, playlist_id):
    if request.method == "GET":
        songlist = Songlist.objects.filter(playlist_id=playlist_id)
        songs = []

        for songlist in songlist:
            song = Song.objects.filter(id=songlist.song_id)
            songs += song
        songs = serializers.serialize("json", songs)
        songs = json.loads(songs)
        return Response(songs)
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})
