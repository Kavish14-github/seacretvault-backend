from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from django.conf import settings

from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.SECRET_KEY.encode())


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Environment(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class Secret(models.Model):
        # your existing fields...
    key = models.CharField(max_length=255)
    value = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.value and not self.value.startswith("gAAAA"):
            self.value = fernet.encrypt(self.value.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_value(self):
        try:
            return fernet.decrypt(self.value.encode()).decode()
        except Exception:
            return None
