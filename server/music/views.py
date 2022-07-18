from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import os
import json
from model.models import *
from model.views import model
from server.settings import BASE_DIR, get_secret

# Create your views here.
@method_decorator(csrf_exempt)
def music(request):
    if request.method == "POST":
        upload = request.FILES.get("upload_image")
        if upload is None:
                    return JsonResponse({"status":"error", "message":"No image provided"})
        img = Image(image = upload)
        img.save()
    
        ### 사용자가 입력한 장르 ###
        genre = request.POST.get("genre")

        ### 모델에서 키워드, 장르 따오기 ###
        keyword = model(img.id)

        ### 검색 전 키 파일 읽기 ###
        secret_file = os.path.join(BASE_DIR, 'key.json')
        with open(secret_file) as f:
            secrets = json.loads(f.read())

        ### spotify API access ###
        client_id = get_secret("CLIENT_ID", secrets)
        client_secret = get_secret("CLIENT_SECRET", secrets)
        endpoint = "https://accounts.spotify.com/api/token"
        encoded = base64.b64encode("{}:{}".format(
            client_id, client_secret).encode('utf-8')).decode('ascii')
        headers = {"Authorization": "Basic {}".format(encoded)}
        payload = {"grant_type": "client_credentials"}
        response = requests.post(endpoint, data=payload, headers=headers)
        access_token = json.loads(response.text)['access_token']
        headers = {"Authorization": "Bearer {}".format(access_token)}

        # Spotify 음악 검색
        params = {
            "q": keyword + " genre: " + genre,
            "type": "track",
            "limit": "20"
        }
        r = requests.get("https://api.spotify.com/v1/search",
                        params=params, headers=headers)
        results = json.loads(r.text)


        data = {}
        data['status'] = "success" # 성공/실패 여부
        data['image'] = img.image.url # 이미지 url
        data['music'] = [] # 음악 목록
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'], track['preview_url'], track['album']['images'][0]['url'], track['artists'][0]['name'], track['album']['name'], track['id'], track['duration_ms'])
            data['music'].append({
                "title": track['name'],
                "image_album":  track['album']['images'][0]['url'],
                "file": track['preview_url'],
                "artist": track['artists'][0]['name'],
                "title_album": track['album']['name'],
                "id": track['id'],
                "duration": track['duration_ms']
            })
        return JsonResponse(data)

    else:
        return JsonResponse({"status":"error", "message":"Bad request"})