from . import views

from django.urls import path
urlpatterns = [
    path('',views.index,name='home'),
    path('red/',views.redirectt,name='redi'),
    path('ref/',views.refresh_token,name='ref'),
    path('saved/',views.savedpage,name='saved'),
    path('play/<str:uri>',views.play_song,name='play'),
    path('downloads/<str:spotify_id>',views.album_page,name='saved_albums'),
    path('dowloads/<str:playlist_id>',views.playlist_page,name='saved_playlists'),
    path('pause/',views.pause_song,name='pause'),
    path('skip/',views.skip_to_next,name='skip'),
    path('previous/',views.skip_to_previous,name='previous'),
    path('searchview/',views.search_view,name='search_view'),

]