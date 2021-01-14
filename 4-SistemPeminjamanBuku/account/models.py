from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, fullname, phone, status, is_staff, is_active, password,
    **extra_fields):

        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(  email=email,
                            fullname=fullname,
                            phone=phone,
                            status=status,
                            is_staff=is_staff,
                            is_active=is_active,
                            **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self,  email, fullname, phone, status,  is_staff, is_active,password=None, **extra_fields):
        return self._create_user(email, fullname, phone, status, is_staff,True, password, **extra_fields)

    def create_superuser(self, email, fullname, phone, status, is_staff,is_active,password=None, **extra_fields):
        return self._create_user(email, fullname, phone, "ADMIN",  True, True, password,  **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    created_on = models.DateTimeField(default=datetime.datetime.now)
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    STATUS_USER = (
        ("ADMIN", "ADMIN"),
        ("STUDENT", "STUDENT"),
    )
    status = models.CharField(max_length=50, choices=STATUS_USER, default="STUDENT")
    tanggal_lahir = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone', 'status','is_active', 'is_staff',]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.status == 'ADMIN':
            self.is_staff = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{} / {}'.format(self.fullname, self.email)
