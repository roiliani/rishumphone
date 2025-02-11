from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier for authentication instead of username."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)  # Make email unique and required
    first_name = models.CharField(max_length=30, blank=True, null=True)  # Add first name
    last_name = models.CharField(max_length=30, blank=True, null=True)  # Add last name
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Set email as the primary identifier
    REQUIRED_FIELDS = ["first_name", "last_name"]  # These fields are required when creating a superuser

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
