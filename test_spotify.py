
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import pandas as pd


# connect to the API
client_id = 'your_id'
client_secret = 'your_secret'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = getTrackIDs('profilename', 'playlist_id') 

def getTrackFeatures(id):
      meta = sp.track(id)
      features = sp.audio_features(id)

      # meta
      name = meta['name']
      album = meta['album']['name']
      artist = meta['album']['artists'][0]['name']
      release_date = meta['album']['release_date']

      track = [name, album, artist, release_date]
      return track

#loop over track ids to create dataset
tracks = []
for i in range(0,len(ids)):
    time.sleep(.5)
    track = getTrackFeatures(ids[i])
    tracks.append(track)

df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date'])

df.to_csv("file_name.csv", sep = ',')
