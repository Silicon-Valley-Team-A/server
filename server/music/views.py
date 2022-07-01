from django.shortcuts import render
import requests
import base64
from pathlib import Path
import os, json
import sys

# Create your views here.
def api(request):
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
        "q": "BTS",
        "type": "artist",
        "limit": "1"
    }

    r = requests.get("https://api.spotify.com/v1/search",
                    params=params, headers=headers)

    print(r.text)
    print(r.status_code)
    print(r.headers)

    raw = json.loads(r.text)
    artist_raw = raw['artists']['items'][0]
    print(artist_raw)

    genres = artist_raw['genres']
    href = artist_raw['href']

    print("genres: " + str(genres))
    print("href: " + str(href))