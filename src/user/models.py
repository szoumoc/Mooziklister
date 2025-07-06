
from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    spotify_id = models.OneToOneField(
        'spotifyUserProfile.SpotifyUserProfile',
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=True,
        blank=False
    )

    def __str__(self):
        return str(self.username)