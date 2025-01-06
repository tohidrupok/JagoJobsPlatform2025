from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    #related_name 
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions", 
        blank=True,
    ) 
    
    @property
    def is_seeker(self):
        return self.role == 'seeker'

    @property
    def is_employer(self):
        return self.role == 'employer'
    
    @property
    def is_manager(self):
        return self.role == 'manager'