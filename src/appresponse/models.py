from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class AppResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.UUIDField(db_index=True, default=uuid.uuid4)
    user_input = models.TextField()
    llm_response = models.JSONField()
    confirmed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.session_id}"