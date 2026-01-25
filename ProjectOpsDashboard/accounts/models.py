from django.contrib.auth.models import AbstractUser
from django.db import models
from core import constants

class User(AbstractUser):   # AbstractUser has the Django default user fields.
    role = models.CharField(
        max_length=20,
        choices=constants.USER_ROLE,
        default='member'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_manager(self):
        return self.role == 'manager'
    
    def is_member(self):
        return self.role == 'member'
    
    def __str__(self):
        return f"{ self.username } ({ self.role })"