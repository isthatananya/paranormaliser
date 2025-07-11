from django.db import models

# Create your models here.

class ModelAccessHistory(models.Model):
    model_name = models.CharField(max_length=255)
    access_time = models.DateTimeField(auto_now_add=True)
    accessed_by = models.CharField(max_length=255)
    attempts_count = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.model_name} accessed by {self.accessed_by} at {self.access_time}"
    
    @property
    def is_accessible(self):
        # Logic to determine if the model can be accessed
        return self.attempts_count > 0