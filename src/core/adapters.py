# myapp/adapters.py
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from spotifyUserProfile.models import SpotifyUserProfile  # Import your model

class CustomSpotifyOAuth2Adapter(OAuth2Adapter):
    provider_id = "spotify"
    access_token_url = "https://accounts.spotify.com/api/token"
    authorize_url = "https://accounts.spotify.com/authorize"
    profile_url = "https://api.spotify.com/v1/me"

    def complete_login(self, request, app, token, **kwargs):
        print(f"✅ Access token: {token.token}")
        print(f"🔄 Refresh token: {token.token_secret}")  # This is the refresh token

        # Your fix: Adding proper headers
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }

        resp = get_adapter().get_requests_session().get(
            self.profile_url, 
            headers=headers
        )
        print(f"📡 Spotify /me response: {resp.status_code} - {resp.text}")

        resp.raise_for_status()
        extra_data = resp.json()
        
        # Store or update the user profile with tokens
        spotify_user_profile, created = SpotifyUserProfile.objects.update_or_create(
            spotify_id=extra_data.get('id'),
            defaults={
                'email': extra_data.get('email', ''),
                'access_token': token.token,
                'refresh_token': token.token_secret or '',  # token_secret contains refresh token
            }
        )
        
        if created:
            print(f"🆕 Created new SpotifyUserProfile for {extra_data.get('id')}")
        else:
            print(f"🔄 Updated SpotifyUserProfile for {extra_data.get('id')}")
        
        return self.get_provider().sociallogin_from_response(request, extra_data)

# Views using your custom adapter
oauth_login = OAuth2LoginView.adapter_view(CustomSpotifyOAuth2Adapter)
oauth_callback = OAuth2CallbackView.adapter_view(CustomSpotifyOAuth2Adapter)