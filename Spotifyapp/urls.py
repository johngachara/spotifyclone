from . import views

from django.urls import path
urlpatterns = [
    path('',views.index,name='home'),
    path('red/',views.redirectt,name='redi'),
    path('ref/',views.refresh_token,name='ref'),
]