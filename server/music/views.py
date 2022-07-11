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

import urllib3
from .models import *

# Create your views here.

def main(request):
    return HttpResponse("Hi there!")

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
        "q": "sea" + "energy: 0.7, genre: rock",
        "type": "track",
        "limit": "10"
    }

    r = requests.get("https://api.spotify.com/v1/search",
                     params=params, headers=headers)

    results = json.loads(r.text)

    data = {}
    data['musics'] = []
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'], track['preview_url'], track['album']['images'][0]['url'], track['artists'][0]['name'], track['album']['name'], track['id'], track['duration_ms'])
        data['musics'].append({
            "title": track['name'],
            "img_url":  track['album']['images'][0]['url'],
            "music_url": track['preview_url'],
            "artists": track['artists'][0]['name'],
            "album_name": track['album']['name'],
            "id": track['id'],
            "duration_ms": track['duration_ms']
        })

    return HttpResponse(data['musics'], content_type="application/json")