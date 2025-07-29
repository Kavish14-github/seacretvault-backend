from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os
from django.conf import settings

# Generate and store a single encryption key per instance (you might store this more securely in production)
FERNET_KEY = os.environ.get('FERNET_KEY', Fernet.generate_key())
f = Fernet(FERNET_KEY)

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
        if self.value and not self.value.startswith("gAAAA"):  # naive check to avoid re-encrypting
            fernet = Fernet(settings.FERNET_KEY.encode())
            self.value = fernet.encrypt(self.value.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_value(self):
        try:
            fernet = Fernet(settings.FERNET_KEY.encode())
            return fernet.decrypt(self.value.encode()).decode()
        except Exception:
            return None 
