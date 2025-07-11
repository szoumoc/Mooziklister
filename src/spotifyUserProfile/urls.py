from django.urls import path
from core.adapters import oauth_login, oauth_callback

urlpatterns = [
    path("login/", oauth_login, name="spotify_login"),
    path("login/callback/", oauth_callback, name="spotify_callback"),
]
