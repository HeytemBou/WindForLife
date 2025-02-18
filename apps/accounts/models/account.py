# Django imports
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

# Local imports
from uuid import uuid4

# Models
from apps.accounts.models.time_stamped_model import TimeStampedModel


class CustomUserManager(BaseUserManager):
    """Custom user manager model that implements: create_user, create_superuser and create_staff_user"""

    def create_user(self, email: str, password: str, **extra_fields):
        # creates, saves and returns a `User` with email, and password
        if not email:
            raise ValueError('Email must be set for user')

        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.save(using=self._db)  # using=self._db is required for supporting multiple databases with Django

        return account

    def create_superuser(self, email: str, password: str, **extra_fields):
        # creates, saves and returns a `User` with email, and password
        if not email:
            raise ValueError('Email must be set for superuser')

        account = self.model(email=self.normalize_email(email), **extra_fields)
        account.set_password(password)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.save(using=self._db)
        return account


#########################################
#             Account model             #
#########################################
class Account(AbstractBaseUser, TimeStampedModel):
    """Custom user model that implements: email, is_email_verified, is_active, is_staff, is_admin, is_superuser"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True,
                              verbose_name='email',
                              max_length=255,
                              error_messages={"unique": "A user with that email already exists."})

    # These are roles specific to the website
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email and password are required by default

    class Meta:
        db_table = 'accounts'

    def has_perm(self, perm, obj=None):
        return self.is_admin and self.is_active

    def has_module_perms(self, app_label):
        return self.is_admin and self.is_active

