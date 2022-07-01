from django.shortcuts import render
import requests
import base64
import json
import sys
# Create your views here.
def api(request):
    client_id = "189ac73270fc4c9fafc4bd9fff449099"
    client_secret = "a3a2ccf602c6469da4889bc3aa07e450"
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