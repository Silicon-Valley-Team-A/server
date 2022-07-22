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

        if 'songs' in data:
            for s in data.get('songs'):
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
            playlist_obj.delete()
            return JsonResponse({"status":"error", "message":"no music data"})
    else: 
        return JsonResponse({"status":"error", "message":"Bad request"})


def playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id=data.get('user_id')
        if user_id is None:
            return JsonResponse({"status":"error", "message":"You need to login first"})

        result = {}

        # 사용자 이름 가져오는 부분
        try:
            user = User.objects.get(id=user_id)
            result['username'] = user.name
        except User.DoesNotExist:
            return JsonResponse({"status":"error", "message":"You need to login first"})


        # 플레이리스트 정보 가져오는 부분
        if Playlist.objects.filter(user=user_id).exists():
            playlists = Playlist.objects.filter(user=user_id)

            serializer = PlaylistSerializer(instance=playlists, many=True)
            dumped = json.dumps(serializer.data)
            result['playlist'] = json.loads(dumped)

            image = []
            for playlist in playlists:
                # 상위 4개 앨범아트 가져오는 부분
                songlist = Songlist.objects.filter(playlist=playlist.id)
                cnt = 0
                urllist = []
                for songdata in songlist.iterator():
                    if cnt > 3:
                        break

                    song = Song.objects.get(id=songdata.song.id)
                    urllist.append(song.image_album)
                    cnt += 1
                    
                image.append({
                    playlist.id:urllist
                })
            result['image'] = image

            return JsonResponse(result, content_type="text/json-comment-filtered")
        else:
            result["status"] = "success"
            result["message"] = "success but no playlists"
            return JsonResponse(result, content_type="text/json-comment-filtered") 
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
