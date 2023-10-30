import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
import base64

client_id = '2ee2d0c4a9494a7c8f3df35ca82b009k087'
client_secret = '68d6e1fa37a24e07bf5b525e4bb1ko01492'


def index(request):
    URL = 'https://accounts.spotify.com/authorize'
    response_type = 'code'
    redurl = 'http://127.0.0.1:8000/red'
    scope = 'user-read-private user-read-email user-modify-playback-state user-library-read user-read-playback-state user-read-recently-played'
    state = "state"
    spotify_url = f"{URL}?response_type={response_type}&client_id={client_id}&scope={scope}&redirect_uri={redurl}&state={state}"
    return redirect(spotify_url)


def refresh_token(request):
    refresh_token = request.session.get('refresh_token')

    if refresh_token:
        auth_str = f'{client_id}:{client_secret}'
        auth_bytes = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }

        headers = {
            'Authorization': f'Basic {auth_bytes}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        token_url = 'https://accounts.spotify.com/api/token'
        response = requests.post(token_url, data=data, headers=headers)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')

            # Update the stored access token
            request.session['access_token'] = access_token

    return redirect('redirectt')  # Redirect to your existing view


def redirectt(request):
    code = request.GET.get('code')
    if not code:
        print(code)
    auth_str = f'{client_id}:{client_secret}'
    auth_bytes = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/red'
    }

    headers = {
        'Authorization': f'Basic {auth_bytes}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')

        # Store the tokens securely (e.g., in a database or a secure configuration)
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token

    recenturls = 'https://api.spotify.com/v1/me/player/recently-played'
    params = {
        "limit": 15
    }
    access_token = request.session.get('access_token')
    headers2 = {
        "Authorization": "Bearer " + access_token
    }
    res2 = requests.get(recenturls, headers=headers2, params=params).json()
    songs = res2['items'][0]['track']['album']['images'][0]['url']
    name = res2['items'][0]['track']['album']['name']
    songs2 = res2['items'][1]['track']['album']['images'][0]['url']
    name2 = res2['items'][1]['track']['album']['name']
    songs3 = res2['items'][2]['track']['album']['images'][0]['url']
    name3 = res2['items'][2]['track']['album']['name']
    songs4 = res2['items'][3]['track']['album']['images'][0]['url']
    name4 = res2['items'][3]['track']['album']['name']
    songs5 = res2['items'][4]['track']['album']['images'][0]['url']
    name5 = res2['items'][4]['track']['album']['name']
    songs6 = res2['items'][5]['track']['album']['images'][0]['url']
    name6 = res2['items'][5]['track']['album']['name']
    songs7 = res2['items'][6]['track']['album']['images'][0]['url']
    name7 = res2['items'][6]['track']['album']['name']
    songs8 = res2['items'][7]['track']['album']['images'][0]['url']
    name8 = res2['items'][7]['track']['album']['name']
    songs9 = res2['items'][8]['track']['album']['images'][0]['url']
    name9 = res2['items'][8]['track']['album']['name']
    return render(request, 'red.html', {"image": songs, "name": name,"image2": songs2, "name2": name2,"image3": songs3, "name3": name3,"image4": songs4, "name4": name4,"image5": songs5, "name5": name5,"image6": songs6, "name6": name6,"image7": songs7, "name7": name7,"image8": songs8, "name8": name8,"image9": songs9, "name9": name9})



# ... Your other views and code
