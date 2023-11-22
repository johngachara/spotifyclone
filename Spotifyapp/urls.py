from . import views

from django.urls import path
urlpatterns = [
    path('',views.index,name='home'),
    path('red/',views.redirectt,name='redi'),
    path('ref/',views.refresh_token,name='ref'),
    path('saved/',views.savedpage,name='saved'),
    path('play/<str:uri>',views.play_song,name='play'),
    path('downloads/<str:spotify_id>',views.album_page,name='saved_albums')

]