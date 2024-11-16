from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def __str__(self) -> str:
        return f"User {self.username} {self.email} ({self.id})"

#class x(models.Model):