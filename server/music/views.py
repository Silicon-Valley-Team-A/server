from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
import json
import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from model.models import *
from model.views import model
from server.settings import BASE_DIR, get_secret, INTERNAL_HOST_IP

# Create your views here.

### 노래 개수가 20개를 넘지 않도록 함 ###
IS_FULL = False

### 노래 검색 결과를 적절한 형식에 맞게 변환 ###
def search_songs(results):
    data = {}
    data['music'] = []
    for idx, track in enumerate(results['tracks']['items']):
        try:
            if(not (track['preview_url']==None)):
                data['music'].append({
                    "title": track['name'],
                    "image_album":  track['album']['images'][0]['url'],
                    "file": track['preview_url'],
                    "artist": track['artists'][0]['name'],
                    "title_album": track['album']['name'],
                    "id": track['id'],
                    "duration": track['duration_ms']
                })
        except:
            pass
    return data

### 노래의 특성 얻는 함수 ###
def get_features(sp, track_id):
    # get audio_feature
    features = sp.audio_features(tracks=[track_id])
    try:
        #acousticness = features[0]["acousticness"]
        danceability = features[0]["danceability"]
        energy = features[0]["energy"]
        #liveness = features[0]["liveness"]
        #loudness = features[0]["loudness"]
        valence = features[0]["valence"]
        #mode = features[0]["mode"]
        tempo = features[0]["tempo"]

        result = {"danceability" : danceability,
                    "energy" : energy,
                    "valence" : valence,
                    "tempo" : tempo}
    except:
        pass

    return result
    
### 각 음악을 분위기에 따라 분류, 해당 분위기의 기준을 충족하면 추가! ###
def music_classification(sp, data, res, key):
    cnt = 0
    for classify in data['music']:
        result = get_features(sp, classify['id'])
        cnt += 1
        if(key['mood']=="happy"):
            if(result['danceability']>0.7 or result['energy']>0.7 or result['valence']>0.7 or result['tempo']>100):
                res['music'].append(classify)
            else:
                pass
        elif(key['mood']=="sad"):
            if(result['danceability']<0.4 or result['energy']<0.4 or result['valence']<0.4 or result['tempo']<90):
                res['music'].append(classify)
            else:
                pass
        elif(key['mood']=="scary"):
            if(result['danceability']<0.7 or result['danceability']>0.4 or result['energy']>0.7 or result['valence']<0.4 or result['tempo']>100):
                res['music'].append(classify)
            else:
                pass
        if (len(res['music']) >= 20):
            IS_FULL = True
            break
    return res


@method_decorator(csrf_exempt)
def music(request):
    if request.method == "POST":
        # 전역변수 설정
        IS_FULL = False

        ### 이미지 파일 데이터베이스에 저장 ###
        upload = request.FILES.get("upload_image")
        if upload is None:
            return JsonResponse({"status":"error", "message":"No image provided"})
        img = Image(image = upload)
        img.save()
    
        ### 사용자가 입력한 장르 ###
        genre = request.POST.get("genre")

        ### 모델에서 키워드(keyword), 분위기(mood) 따오기 ###
        key = model(img.id)

        ### 검색 전 키 파일 읽기 ###
        secret_file = os.path.join(BASE_DIR, 'key.json')
        with open(secret_file) as f:
            secrets = json.loads(f.read())

        ### spotify API access ###
        birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
        client_id = get_secret("CLIENT_ID", secrets)
        client_secret = get_secret("CLIENT_SECRET", secrets)
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # 리턴값 선언
        res = {}
        res['music'] = []


        # Spotify 음악 검색
        ### 장르의 입력 여부에 따라 음악을 검색 ###
        for i in range(0, 4):
            if(genre == ''):
                results = sp.search(q=key['keyword'][i], limit=30)
            else:
                results = sp.search(q=key['keyword'][i]+" genre: "+genre, limit=30)
            data = search_songs(results) # 검색 결과를 우선 형식에 맞게 변환하여 data로 저장
            res = music_classification(sp, data, res, key) # data에서 분위기에 맞는 음악만을 따로 추출해서 res에 저장
            if IS_FULL:
                break


        res['status'] = "success" # 성공/실패 여부
        res['image'] = INTERNAL_HOST_IP+urllib.parse.unquote(img.image.url) # 이미지 url
        return JsonResponse(res)
    else:
        return JsonResponse({"status":"error", "message":"Bad request"})