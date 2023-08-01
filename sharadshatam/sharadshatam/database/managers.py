from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _

# from .models import *

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given phone and password.
        """
        if not username:
            raise ValueError('The phone must be provided')
        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.is_staff = True
        
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user