from multiprocessing.sharedctypes import Value
import uuid
from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class UserAccountManager(BaseUserManager):
    """UserManager class"""

    def create_user(self, email: str, name: str, password: Optional[str] = None):

        if name is None:
            raise ValueError("Name must be present")

        if email is None:
            raise ValueError("User must have email address")

        email = self.normalize_email(email)
        # Manager class has an attribute .model
        user = self.model(email=email, name=name)
        user.set_password(password)
        # if you have more than one db use self._db
        user.save()
        return user

    # from manager classes, defining user and superuser fields
    # will be providing the password
    def create_superuser(self, email: str, name: str, password: str):
        """Create and return a `User` with superuser (admin)"""
        if password is None:
            raise ValueError("Superusers must have a password")

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


# create custom user model
class UserAccount(AbstractBaseUser, PermissionsMixin):

    # authenticate user by email
    # id = models.UUIDField(primary_key = True, default =uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    name = models.CharField(db_index=True, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    # Tells Django that the UserAccountManager class defined above should manage
    # objects of this type.
    objects = UserAccountManager()

    # methods from User class
    def get_full_name(self):
        """Return full name of the user"""
        return self.name

    def get_short_name(self):
        """Return short name of the user"""
        return self.name

    def __str__(self):
        """Return a string representation of this user"""
        string = self.email if self.email != "" else self.get_full_name()
        return f"{self.id} {string}"

    @property
    def tokens(self):
        """Allow us to get user's token"""
        # for_user add this token to outstanding token list
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
