import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from instagrapi import Client

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-currently-playing user-read-playback-state"
))

cl = Client()
cl.login("username", "password")

def update_instagram_bio(track_name, artists, progress_ms, duration_ms):
    progress_seconds = progress_ms / 1000
    duration_seconds = duration_ms / 1000
    progress_min, progress_sec = divmod(int(progress_seconds), 60)
    duration_min, duration_sec = divmod(int(duration_seconds), 60)
    progress_steps = 10
    if duration_seconds > 0:
        progress_bar = "🟩" * min(progress_steps, int(progress_steps * (progress_seconds / duration_seconds))) + \
                       "⬜" * (progress_steps - min(progress_steps, int(progress_steps * (progress_seconds / duration_seconds))))
    else:
        progress_bar = "⬜" * progress_steps
    new_bio = (
        f"🎶 En train d'écouter: {track_name}\n"
        f"👤 Artiste: {artists}\n"
        f"⏳ Temps: {progress_min}:{progress_sec:02d} / {duration_min}:{duration_sec:02d}\n"
        f"{progress_bar} {progress_seconds:.0f}s"
    )
    if len(new_bio) > 150:
        new_bio = new_bio[:147] + "..."
    cl.account_edit(biography=new_bio)
    print(f"Bio mise à jour : {new_bio}")

previous_track = None

while True:
    try:
        current_track = sp.current_playback()
        if current_track is not None and current_track['is_playing']:
            track_name = current_track['item']['name']
            artists = ", ".join([artist['name'] for artist in current_track['item']['artists']])
            progress_ms = current_track['progress_ms']
            duration_ms = current_track['item']['duration_ms']
            if previous_track != track_name:
                update_instagram_bio(track_name, artists, progress_ms, duration_ms)
                previous_track = track_name
            else:
                update_instagram_bio(track_name, artists, progress_ms, duration_ms)
        time.sleep(5) #High risk of being limited..
    except Exception as e:
        print(f"Erreur rencontrée : {e}")
        time.sleep(60)
