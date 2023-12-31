import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import requests
import base64
from django.contrib import messages

from django.urls import reverse

client_id = '1fd1b686693d4568a6905422d631ea10'
client_secret = 'a746a404e72a43a2b41272da3a64ed21'


def index(request):
    URL = 'https://accounts.spotify.com/authorize'
    response_type = 'code'
    redurl = 'http://127.0.0.1:8000/red'
    scope = 'playlist-read-private user-read-private user-read-email user-modify-playback-state user-library-read user-read-playback-state user-read-recently-played streaming user-read-currently-playing'
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
        "limit": 20
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
        type = album.get('type','')
        artists = track.get('artists','')[0]
        artist_name = artists.get('name','')
        spotifyuri = album.get('uri','')
        artistid = artists['id']
        timez = item.get('played_at','')
        artist_info.append(artistid)
        songs_info.append({"image":url,"name":name,"artist_name":artist_name,"time":timez,"uri":spotifyuri,"type":type})
    featuredurl = 'https://api.spotify.com/v1/browse/featured-playlists'
    params2 = {"locale":"","limit":20}
    featuredlist = []
    response2 = requests.get(featuredurl,params=params2,headers=headers2).json()
    playlist = response2.get('playlists','')
    for items in playlist.get('items',[]):
        image2 = items.get('images','')[0]
        url2 = image2.get('url','')
        name2 = items.get('name','')
        spotifyuri2 = items.get('uri','')
        featuredlist.append({"image":url2,"name":name2,"uri":spotifyuri2})
    recent_tracks_url = 'https://api.spotify.com/v1/me/playlists'
    response3 = requests.get(recent_tracks_url,params={"limit":20},headers=headers2).json()
    items3 = response3.get('items',[])
    recent_playlist = []
    for e in items3:
        image3 = e.get('images','')[0]
        url3 = image3.get('url','')
        name3 = e.get('name','')
        uri = e.get('uri','')
        recent_playlist.append({"image":url3,"name":name3,"uri":uri})


    return render(request, 'red.html', {"data":songs_info,
                                        "access_token":access_token,
                                        "featured":featuredlist,"recent":recent_playlist})
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
        playlist_id = item.get('id','')
        uri = item.get('uri','')
        saved_items.append({"name":name,"descr":descr,"pic":pic,"playlist_id":playlist_id,"uri":uri})
    saved_albums_url = 'https://api.spotify.com/v1/me/albums'
    response2 = requests.get(saved_albums_url,params={"limit":20},headers=headers).json()
    items2 = response2.get('items',[])
    saved_albums = []
    for i in items2:
        album = i.get('album','')
        image = album.get('images','')[0]
        spotify_id = album.get('id','')
        url = image.get('url','')
        album_name = album.get('name','')
        album_uri = album.get('uri','')
        saved_albums.append({"image":url,"name":album_name,"spotify_id":spotify_id,"uri":album_uri})



    return render(request,'saved.html',{"data":saved_items,"saved_albums":saved_albums})
def play_song(request,uri):
    play_url = 'https://api.spotify.com/v1/me/player/play'
    params = {"context_uri":uri,"device_id":""}
    access_token = request.session.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.put(play_url,json=params,headers=headers)
    if response:
        return redirect('redi')
    else:
        messages.error(request,"Connect to spotify device to play music")
        return redirect('redi')


def album_page(request,spotify_id):
    access_token = request.session.get('access_token')
    track_url = f"https://api.spotify.com/v1/albums/{spotify_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(track_url,params={"limit":40},headers=headers).json()
    items = response.get('items',[])
    albums = []
    for i in items:
        name = i.get('name','')
        artist = i.get('artists','')[0]
        uri = artist.get('uri','')
        artist_name = artist.get('name','')
        albums.append({"name":name,"uri":uri,"artist_name":artist_name})
    return render(request,'albums.html',{"data":albums,"uri":uri})
def playlist_page(request,playlist_id):
    access_token = request.session.get('access_token')
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(playlist_url,headers=headers,params={"limit":20}).json()
    items = response.get('items',[])
    tracks = []
    for item in items:
        track = item.get('track','')
        album = track.get('album','')
        images = album.get('images','')[0]
        url = images.get('url','')
        name = track.get('name','')
        name2 = album.get('name','')
        uri = album.get('uri','')
        artist = album.get('artists','')[0]
        artist_name = artist.get('name','')
        tracks.append({"name":name,"uri":uri,"artist_name":artist_name,"album":name2})
    return render(request,'albums.html',{"data":tracks,"uri": uri})
def pause_song(request):
    pause_url = 'https://api.spotify.com/v1/me/player/pause'
    access_token = request.session.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"device_id":""}
    response = requests.put(pause_url,json=params,headers=headers)
    if response:
        redirect_url = reverse('redi')
        return HttpResponseRedirect(redirect_url)
    else:
        messages.error(request,"No device / song Playing")
        return redirect('redi')



def skip_to_next(request):
    skip_url = 'https://api.spotify.com/v1/me/player/next'
    access_token = request.session.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"device_id": ""}
    response = requests.post(skip_url,json=params,headers=headers)
    if response:
        redirect_url = reverse('redi')
        return HttpResponseRedirect(redirect_url)
    else:
        messages.error(request,"No device / song Playing")
        return redirect('redi')


def skip_to_previous(request):
    skip_url = 'https://api.spotify.com/v1/me/player/previous'
    access_token = request.session.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"device_id": ""}
    response = requests.post(skip_url,json=params,headers=headers)
    if response:
        redirect_url = reverse('redi')
        return HttpResponseRedirect(redirect_url)
    else:
        messages.error(request,"No device / song Playing")
        return redirect('redi')

def search_view(request):
    if 'searchform' in request.POST:
        searching = request.POST['searchform']
    else:
        searching = 'jah jah dont leave me'

    search_url = 'https://api.spotify.com/v1/search'
    access_token = request.session.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"q": searching, "type": ['track', 'album', 'artist', 'playlist'], "limit": 20,
              "include_external": "audio"}
    response = requests.get(search_url, headers=headers, params=params).json()
    tracks = response.get('tracks','')
    album = tracks.get('items',[])
    tracks_dict = []
    for item in album:
        name = item.get('name','')
        album_items = item.get('album','')
        uri = album_items.get('uri','')
        artist = album_items.get('artists','')[0]
        artist_name = artist.get('name','')
        image = album_items.get('images','')[0]
        url = image.get('url','')
        tracks_dict.append({"name":name,"image":url,"uri":uri,"artist_name":artist_name})
    return render(request,'search.html',{"data":tracks_dict})


