from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    playlist_url = models.URLField(max_length=200)
    playlist_name = models.CharField(max_length=100)
    playlist_desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='playlist_images/', blank=True, null=True)
    track_fk_id = models.CharField(max_length=50, blank=True, null=True)
    visibility = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_url = models.URLField(max_length=200)
    name = models.CharField(max_length=200)
    singer = models.CharField(max_length=100)
    duration = models.DurationField(help_text="Track duration in HH:MM:SS format")
    image_cover_url = models.URLField(max_length=200, blank=True, null=True)
    in_playlist = models.ManyToManyField(Playlist)

    def __str__(self):
        return str(self.id)