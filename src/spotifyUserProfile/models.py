from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class SpotifyUserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    spotify_user_id = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='spotify_profile')

    def __str__(self):
        return f"{self.user.username} - {self.spotify_user_id}"
    

class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class PlaylistSpotifyResponse(models.Model):
    pass

class PlaylistTrack(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks') #stores the playlist this track belongs to
    position = models.IntegerField(blank=True, null=True)  # i might not need this
    uris = models.JSONField()  # Stores list of track/episode URIs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Track in {self.playlist_id.name} at position {self.position if self.position is not None else 'N/A'}"


class PlaylistImage(models.Model):

    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='images') #the playlist, image belongs to
    image = models.ImageField(upload_to='playlist_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.playlist_id.name}"
    




