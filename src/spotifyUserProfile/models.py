from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class SpotifyUserProfile(models.Model):
    id = models.AutoField(primary_key = True)
    spotify_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(default="")
    access_token = models.TextField(default="")
    refresh_token = models.TextField(default="")

    def __str__(self):
        return self.spotify_id
    

class Create_Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_user_id = models.ForeignKey(SpotifyUserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    playlist_uri = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Spotify URI for the playlist

    def __str__(self):
        return self.name
    

class PlaylistSpotifyResponse(models.Model):
    pass



# Possibly the rest will be KV pair


class add_these_tracks(models.Model):
    id= models.AutoField(primary_key=True)
    playlist_id = models.ForeignKey(Create_Playlist, on_delete=models.CASCADE, related_name='tracks') #stores the playlist this track belongs to
    position = models.IntegerField(blank=True, null=True)  # i might not need this
    uris = models.JSONField()  # Stores list of track/episode URIs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Track in {self.playlist_id.name} at position {self.position if self.position is not None else 'N/A'}"


class PlaylistImage(models.Model):
    id= models.AutoField(primary_key=True)
    playlist_id = models.ForeignKey(Create_Playlist, on_delete=models.CASCADE, related_name='images') #the playlist, image belongs to
    image = models.ImageField(upload_to='playlist_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.playlist_id.name}"
    

class TrackQuery(models.Model):
    id = models.AutoField(primary_key = True)
    query = models.CharField(max_length=255)
    type = "track"
    market = "ES"
    limit = 1
    offset = 0
    include_external = "audio"

    def __str__(self):
        return f"{self.query}"
    
class get_track(models.Model):
    id = models.AutoField(primary_key = True)
    track_id = models.CharField(max_length=255)
    query = models.OneToOneField(TrackQuery, on_delete=models.CASCADE, default= 0)

    def __str__(self):
        return f"Track ID: {self.track_id}"





