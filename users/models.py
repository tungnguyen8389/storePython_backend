from django.db import models
from django.contrib.auth.models import AbstractUser

# Danh sách role cho user
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
)

class User(AbstractUser):
    # Thêm trường role để phân quyền
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    # Nếu muốn có thêm số điện thoại hoặc thông tin khác thì thêm ở đây
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
