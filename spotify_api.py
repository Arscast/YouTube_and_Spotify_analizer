# -*- coding: utf-8 -*-
import spotipy
# from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify_client:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    def get_playlists(self, artist, date_range):
        results = self.sp.search(q=artist + ' year:' + date_range, type='track', limit=20)
        tracks = []
        for idx, track in enumerate(results['tracks']['items']):
            print((idx, track['artists'][0]['name'], track['name'], track['album']['release_date'], track['href']))
            tracks.append((idx, track['artists'][0]['name'], track['name'], track['album']['release_date'], track['href']))
        return tracks
