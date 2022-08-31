from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  # make an unprivileged user by default
  level = models.IntegerField(default=300)
  created_at = models.DateTimeField(auto_now_add=True)


