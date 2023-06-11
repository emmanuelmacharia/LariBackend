from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    '''Overrides the creation of the user methods so that the user is validated first before calling the db'''

    def validate_user(self, first_name=None, last_name=None, email=None, phone_numer=None,  password=None) -> bool:
        """
        Validates user information for the create user and create superuser methods
        """
        if not first_name:
            raise ValueError("Users must have a first name")

        if not last_name:
            raise ValueError("Users must have a last name")

        if not email:
            raise ValueError("Users must have an email address")

        if not phone_numer:
            raise ValueError("User must provide a valid phone nuumber")

        if not password:
            raise ValueError("Users must have a password set")

        return True

    def create_user(self, first_name=None, last_name=None, password=None, email=None, phone_number=None, is_active=True, is_superuser=False):
        """
        Creates and returns a user with an email, first_name, lastname, phone_number and password
        """
        # first_name = first_name
        # last_name = last_name
        # email = email
        # phone_number = phone_number
        # password = password
        validated_user = self.validate_user(
            first_name, last_name, email, phone_number, password)

        if not validated_user:
            pass

        user = self.model(first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email), phone_number=phone_number)

        user.is_active = is_active
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name=None, last_name=None, password=None, email=None, phone_number=None):
        """
        Creates and returns the superuser with all the required fields
        """
        validated_user = self.validate_user(
            first_name, last_name, email, phone_number, password)

        if not validated_user:
            pass

        user = self.model(first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email), phone_number=phone_number)
        user.user_verified = True
        user.date_verified = timezone.now()
        user.is_superuser = True
        user.is_admin = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    '''creates a custom user model for Lari'''
    userId = models.AutoField(primary_key=True, editable=False, unique=True)
    first_name = models.CharField(max_length=255, default=False)
    last_name = models.CharField(max_length=255, default=False)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    date_activated = models.DateTimeField(auto_now_add=True)
    user_verified = models.BooleanField(default=False)
    date_verified = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    objects = UserManager()

    def __str__(self):
        return str(self.email)

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def get_email(self):
        '''property to return the email'''
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_email_verified(self):
        '''returns whether the user's email has been verified'''
        return self.user_verified

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
