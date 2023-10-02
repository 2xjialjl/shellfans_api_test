# users/models.py

from django.db import models
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    profile_picture = models.TextField(blank=True)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    privacy_agreement = models.BooleanField(default=False)
    terms_agreement = models.BooleanField(default=False)
    phone_region = models.CharField(max_length=10, blank=True, null=True)
    third_party_registration_source =models.CharField(max_length=255, null=True, blank=True)
    backup_email = models.EmailField(max_length=254, null=True, blank=True)
    is_backup_email_verified = models.BooleanField(default=False)
    security_code = models.CharField(max_length=4, null=True, blank=True)
class VerificationCode(models.Model):
    user_code = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()