from django.http import HttpResponse
from rest_framework import generics, serializers
from rest_framework.response import Response
from django.shortcuts import render
import requests
import base64
from pathlib import Path
import os
import json
import sys
from .models import *

# Create your views here.


def music(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    secret_file = os.path.join(BASE_DIR, 'key.json')

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

    client_id = get_secret("CLIENT_ID")
    client_secret = get_secret("CLIENT_SECRET")
    endpoint = "https://accounts.spotify.com/api/token"

    # python 3.x 버전
    encoded = base64.b64encode("{}:{}".format(
        client_id, client_secret).encode('utf-8')).decode('ascii')

    headers = {"Authorization": "Basic {}".format(encoded)}

    payload = {"grant_type": "client_credentials"}

    response = requests.post(endpoint, data=payload, headers=headers)

    access_token = json.loads(response.text)['access_token']

    headers = {"Authorization": "Bearer {}".format(access_token)}

    # Spotify Search API
    params = {
        "q": "sea" + " genre: rock",
        "type": "track",
        "limit": "10"
    }

    r = requests.get("https://api.spotify.com/v1/search",
                     params=params, headers=headers)

    raw = json.loads(r.text)

    # # 트랙 리스트 출력
    # for idx, track in enumerate(raw['tracks']['items']):
    #     print(idx, track['name'])

    # # 한 트랙 내 정보 확인용 출력
    # print(raw['tracks']['items'][0])

    return HttpResponse(raw['tracks']['items'], content_type="application/json")