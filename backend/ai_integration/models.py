from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ModelAccessHistory(models.Model):
    model_name = models.CharField(max_length=255)
    access_time = models.DateTimeField(auto_now_add=True)
    accessed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    attempts_count = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.model_name} accessed by {self.accessed_by} at {self.access_time}"
    
    @property
    def is_accessible(self):
        return self.attempts_count > 0
    
class ChatHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    user_question = models.TextField()
    model_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_parent = models.BooleanField(default=False)
    parent_chat = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='child_chats')

    def __str__(self):
        return f"Chat by {self.user_id} at {self.timestamp}"