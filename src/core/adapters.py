# myapp/adapters.py (or wherever you keep custom adapters)

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class CustomSpotifyOAuth2Adapter(OAuth2Adapter):
    provider_id = "spotify"
    access_token_url = "https://accounts.spotify.com/api/token"
    authorize_url = "https://accounts.spotify.com/authorize"
    profile_url = "https://api.spotify.com/v1/me"

    def complete_login(self, request, app, token, **kwargs):
        print(f"✅ Access token: {token.token}")

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
        return self.get_provider().sociallogin_from_response(request, extra_data)


# Views using your custom adapter
oauth_login = OAuth2LoginView.adapter_view(CustomSpotifyOAuth2Adapter)
oauth_callback = OAuth2CallbackView.adapter_view(CustomSpotifyOAuth2Adapter)