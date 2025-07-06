from django.shortcuts import render, redirect
import requests
from urllib.parse import urlencode

# Create your views here.
from user.models import BaseModel
from spotifyUserProfile.models import SpotifyUserProfile
from django.contrib.auth import login
from django.conf import settings

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_PROFILE_URL = "https://api.spotify.com/v1/me"

REDIRECT_URI = "http://localhost:8000/spotify/callback/"
SCOPE = "user-read-email"

def spotify_login(request):
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get('code')

    # Exchange code for access token
    token_response = requests.post(SPOTIFY_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    })

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    # Get user profile from Spotify
    profile_response = requests.get(SPOTIFY_PROFILE_URL, headers={
        "Authorization": f"Bearer {access_token}"
    })
    profile_data = profile_response.json()

    spotify_id = profile_data["id"]
    email = profile_data.get("email", "")

    # Get or create Spotify profile
    spotify_profile= SpotifyUserProfile.objects.get(
        spotify_id=spotify_id,
        defaults={
            "email": email,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )
    if not created:
        # Update tokens if needed
        spotify_profile.access_token = access_token
        spotify_profile.refresh_token = refresh_token
        spotify_profile.save()

    # Link or create BaseModel user
    user, created = BaseModel.objects.get_or_create(
        spotify_id=spotify_profile,
        defaults={"username": spotify_id, "password": "app123"}  # dummy password
    )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return redirect("/")
