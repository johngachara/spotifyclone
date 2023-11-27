Spotify Clone Django App Documentation
1. Introduction

Welcome to the Spotify Clone Django App documentation! This app allows users to interact with the Spotify API, fetching and displaying information about recently played tracks, saved playlists, albums, and more.
This is my emobilis web development bootcamp finals project

2. Dependencies
This app relies on the following dependencies:

Django

Requests

Base64

Make sure these are installed in your Django environment.

3. Cloning the Project
To get started, clone the project from the GitHub repository:

git clone https://github.com/johngachara/spotifyclone.git

4. Configuration
Spotify API Credentials

Obtain your Spotify API credentials (client_id and client_secret) and update the client_id and client_secret variables in your views.py file.

You must be a spotify premium user in order for this application to work.

6. Installing Requirements

Navigate to the project directory and install the required dependencies:

cd spotifyclone

pip install -r requirements.txt

6. Authorization

Index View
The index view initiates the Spotify authorization flow, redirecting users to Spotify for authentication.

Refresh Token View
The refresh_token view refreshes the access token using the stored refresh token.

Redirect View
The redirectt view handles the Spotify API redirect, retrieves access and refresh tokens, and fetches recently played tracks.

Saved Page View
The savedpage view fetches and displays saved playlists and albums.

Play Song View
The play_song view plays a selected song on the user's Spotify device.

Album and Playlist Page Views
The album_page and playlist_page views generate pages with detailed information about albums and playlists.

Pause, Skip Views
The pause_song, skip_to_next, and skip_to_previous views control Spotify playback.

Search View
The search_view allows users to search for tracks, albums, artists, and playlists.

7. Error Handling
The app handles errors gracefully, providing appropriate messages to users in case of issues with Spotify API requests or other errors.

9.The Spotify Web Playback SDK is utilized in the app to control playback on Spotify directly from a web browser. This SDK allows the app to interact with the Spotify player, enabling features like playing, pausing, and skipping tracks.

In 'red.html'  template, ive include a script that initializes the Spotify Web Playback SDK. This script sets up a new player instance, provides the necessary access token for authentication, and defines callbacks for when the player is ready or not ready.

Essentially, the Spotify Web Playback SDK facilitates seamless integration between the Django app and the Spotify player, enabling users to control their Spotify playback experience directly from your web application.

For the app to function you must be using spotify on a device and it must be active.
For a device using spotify to be termed as active it must be playing some music otherwise error messages will be displayed with corresponding info.
