from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    national_code = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15)