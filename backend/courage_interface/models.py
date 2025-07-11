from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    last_attempt = models.DateTimeField(default=timezone.now)
    was_success = models.BooleanField(default=False)
    retries = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.user.username} - {'Success' if self.success else 'Failure'} at {self.timestamp}"

