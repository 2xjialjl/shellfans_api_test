# users/models.py

from django.db import models
from django.utils import timezone
class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.TextField(blank=True)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
class VerificationCode(models.Model):
    user_code = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()