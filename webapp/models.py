from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _

from webapp.choices import *

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            ValueError ('Superuser must have is_staff=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=250)
    last_name = models.CharField(_('last name'), max_length=250,blank=True)
    email_confirmed = models.BooleanField(default=False)
    profile = models.ImageField(upload_to='ProfileImage', default='/ProfileImage/admin.jpg')
    user_type = models.CharField(max_length=20, choices=User_Type, default='Admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s" %(self.first_name.title(), self.last_name.title())

class Product(models.Model):
    product_name = models.CharField(max_length=150)
    description = models.CharField(max_length=240)
    url = models.URLField(max_length=250)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" %(self.product_name.title())

class AssignProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    alert = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return "%s" %(self.user.first_name.title())
