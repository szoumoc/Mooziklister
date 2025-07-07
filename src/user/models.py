from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    
    # Connect to the existing socialaccount_socialaccount table
    social_account = models.OneToOneField(
        'socialaccount.SocialAccount',  # This references the existing table
        on_delete=models.CASCADE,
        related_name='base_profile',
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.username)