from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SOCIAL_CHOICES = [
        ('google', 'Google'),
        ('kakao', 'Kakao'),
        # ('naver', 'Naver'),
    ]
    social_type = models.CharField(max_length=20, choices=SOCIAL_CHOICES, blank=True, null=True)
    social_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username