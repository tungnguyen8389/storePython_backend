from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE CHOICES = (
        ("admin", "Admin" ),
        ("customer", "Customer"),
        role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    )
    def __str__(self):
        return self.username