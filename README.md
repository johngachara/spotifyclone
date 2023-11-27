Spotify clone Django App Documentation
1. Introduction
Welcome to the Spotify Django App documentation! This app allows users to interact with the Spotify API, fetching and displaying information about recently played tracks, saved playlists, albums, and more.

2. Dependencies
This app relies on the following dependencies:

Django
Requests
Base64
Make sure these are installed in your Django environment.

3. Configuration
Spotify API Credentials
Obtain your Spotify API credentials (client_id and client_secret) and update the client_id and client_secret variables in your views.py file.

4. Authorization
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

5. Error Handling
The app handles errors gracefully, providing appropriate messages to users in case of issues with Spotify API requests or other errors.

6. Conclusion
Thank you for using the Spotify Django App! If you have any questions, feedback, or suggestions, feel free to reach out.

