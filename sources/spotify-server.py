import pprint
import time
import sys
from unidecode import unidecode
import os
import subprocess

import spotipy
import spotipy.util as util
from spotipy import oauth2

SPOTIPY_CLIENT_ID = 'f53a030ff20c4402882e7662003e2a43'
SPOTIPY_CLIENT_SECRET = '704e01a893944783afb54f90a9f3f571'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback/'
SCOPE = 'user-read-playback-state'
sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE)

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Whoops, need your username!")
    sys.exit(0)

token = util.prompt_for_user_token(username, SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)
    try:
        while True:
            current_song_info = sp.current_user_playing_track()
            if current_song_info is not None:
                current_song = current_song_info['item']['name']

                current_song_artist = ""
                for i in range(len(current_song_info['item']['artists'])):
                    if(i == 0):
                        current_song_artist += current_song_info['item']['artists'][i]['name']
                    else:
                        current_song_artist += ", " + current_song_info['item']['artists'][i]['name']

                #current_song_artist = current_song_info['item']['artists'][0]['name']
                display_song_info_text = current_song + ';' + current_song_artist
                display_song_info_text = unidecode(display_song_info_text)
                with open('/tmp/spotify-current-song', 'w+') as file:
                    contents = file.read().split("\n")
                    file.seek(0)
                    file.truncate()
                    file.write(display_song_info_text)
                time.sleep(0.5)
            else:
                with open('/tmp/spotify-current-song', 'w+') as file:
                    file.seek(0)
                    file.truncate()
                time.sleep(2)
    except KeyboardInterrupt:
        sys.exit(0)
else:
    print("Can't get token for", username)