from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=128, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)