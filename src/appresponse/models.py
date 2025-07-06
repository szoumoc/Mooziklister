from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class AppResponse(models.Model):
    id = models.AutoField(primary_key= True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.UUIDField(db_index=True, default=uuid.uuid4)
    user_input = models.TextField(default=list, help_text="User input text")
    llm_responses = models.JSONField(default=list, help_text="List of LLM response objects")
    confirmed = models.BooleanField(default=False)
    user_feedback = models.BooleanField(default=True, help_text="User feedback on the response")


    def __str__(self):
        return f"{self.session_id}"