from django.shortcuts import render
from .models import TrackQuery, get_track
from decouple import config
import requests
# Create your views here.
chosen_one = TrackQuery.objects.all()
def fetch_all_song_spotify_ids():
    for track in TrackQuery.objects.all():
        fetch_song_spotify_id_single(track)

SPOTIFY_TOKEN = config("SPOTIFY_TOKEN")

def fetch_song_spotify_id_single(track_query):
    query_text = track_query.query.replace(' ', '+')

    url = f"https://api.spotify.com/v1/search?q={query_text}&type=track&limit=1&offset=0&include_external=audio"
    
    headers = {
        'Authorization': f'Bearer {SPOTIFY_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            track_id = data['tracks']['items'][0]['id']
            print(f'{track_id}')
            get_track.objects.update_or_create(
                query=track_query,
                defaults={'track_id': track_id}
            )
            print(f" Saved track {track_id} for query {track_query.id}")
        except (IndexError, KeyError):
            print(f"No track found for: {query_text}")
    else:
        print(f"Spotify API failed for {query_text} — {response.status_code}")