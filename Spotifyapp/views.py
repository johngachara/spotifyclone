from django.shortcuts import redirect, render
import requests
import base64
client_id = '1fd1b686693d4568a6905422d631ea10'
client_secret = 'a746a404e72a43a2b41272da3a64ed21'


def index(request):
    URL = 'https://accounts.spotify.com/authorize'
    response_type = 'code'
    redurl = 'http://127.0.0.1:8000/red'
    scope = 'playlist-read-private user-read-private user-read-email user-modify-playback-state user-library-read user-read-playback-state user-read-recently-played streaming'
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

    return redirect('redirectt')


def redirectt(request):
    code = request.GET.get('code')
    if not code:
        print('wrong code')
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
        "limit": 6
    }
    access_token = request.session.get('access_token')
    headers2 = {
        "Authorization": "Bearer " + access_token
    }
    res2 = requests.get(recenturls, headers=headers2, params=params).json()
    songs_info = []
    artist_info = []
    for item in res2.get('items',[]):
        track = item.get('track','')
        album = track.get('album','')
        image = album.get('images','')[0]
        url = image.get('url','')
        name = track.get('name','')
        artists = track.get('artists','')[0]
        artist_name = artists.get('name','')
        spotifyuri = artists.get('uri','')
        artistid = artists['id']
        timez = item.get('played_at','')
        artist_info.append(artistid)
        songs_info.append({"image":url,"name":name,"artist_name":artist_name,"time":timez,"uri":spotifyuri})
    return render(request, 'red.html', {"data":songs_info,"access_token":access_token})
def savedpage(request):
    playlisturl = 'https://api.spotify.com/v1/me/playlists'
    access_token = request.session.get('access_token')
    headers = {
        "Authorization":f"Bearer {access_token}"
    }
    response = requests.get(playlisturl,headers=headers).json()
    items = response.get('items',[])
    saved_items = []
    for item in items:
        descr = item.get('description','')
        name = item.get('name','')
        pic = item.get('images', [{}])[0].get('url', '')
        saved_items.append({"name":name,"descr":descr,"pic":pic})
    return render(request,'saved.html',{"data":saved_items})
def albumpage(request):
    access_token = request.session.get('access_token')
    albumurl = 'https://api.spotify.com/v1/artists'
    headers = {
        "Authorization":f"Bearer {access_token}"
    }
    ans = requests.get(albumurl,params={"id":ids},headers=headers).json()
    followers = ans.get('name','')
    return render(request,'savedalbum.html',{"f":followers})

