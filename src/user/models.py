
from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    spotify_id = models.CharField(max_length=30, unique=True, blank=False, null=True, help_text="Spotify ID of the user")
    foreign_key_to_playlist = models.CharField(max_length=12, blank=True, null=True, default=list, help_text="Foreign key to playlist, stored as a string")
    
  
  
    def __str__(self):
        return str(self.id)