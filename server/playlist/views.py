from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from account.models import *
from .models import *
import json

# Create your views here.
@method_decorator(csrf_exempt)
def save(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id=data.get('user_id')
        if User.objects.filter(id=user_id).exists():
            user_data = User.objects.get(id=user_id)
        else:
            return JsonResponse({"status":"error", "message":"You need to login first"})            

        playlist_obj = Playlist.objects.create(
            user=user_id,
            name=data.get('name'),
            tag=data.get('tag')
        )
        playlist_obj.save()

        if 'music' in data:
            for s in data.get('music'):
                try:
                    song_obj = Song.objects.get(id=s['id'])
                except Song.DoesNotExist:
                    song_obj = Song.objects.create(id=s['id'],
                                               title=s['title'],
                                               artist=s['artist'],
                                               duration=s['duration'],
                                               file=s['file'],
                                               title_album=s['title_album'],
                                               image_album=s['image_album'])
                    song_obj.save()
    
                songlist_obj = Songlist.objects.create(
                    playlist = playlist_obj,
                    song = song_obj
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
        if Playlist.objects.filter(user=user_id).exists():
            playlists = Playlist.objects.filter(user=user_id)

            serializer = PlaylistSerializer(instance=playlists, many=True)
            result = json.dumps(serializer.data)
            return HttpResponse(result, content_type="text/json-comment-filtered")
        else:
            return JsonResponse({"status":"error", "message":"No playlists"}) 
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})

def showplaylist(request, id):
    if request.method == "GET":
        songlist = Songlist.objects.filter(playlist=id)
        
        songid = []
        for songdata in songlist:
            songid.append(songdata.song.id)

        songs = Song.objects.filter(id__in=songid)
        serializer = SongSerializer(instance=songs, many=True)
        result = json.dumps(serializer.data)
        return HttpResponse(result, content_type="text/json-comment-filtered")
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})
