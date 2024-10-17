from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        indexes = [
            models.Index(fields=["-username"]),
        ]

    def get_absolute_url(self):
        return reverse(
            "user:profile",
            args=[
                self.pk,
            ],
        )

    def __str__(self):
        return self.username
