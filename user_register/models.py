from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
        if not email:
            raise ValidationError(_('You must provide an email address.'))
        email = self.normalize_email(email)
        other_fields.setdefault('is_active', True)
        user = self.model(
            email = email,
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValidationError(_("Superuser must be assigned 'is_superuser = True'"))

        return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name
