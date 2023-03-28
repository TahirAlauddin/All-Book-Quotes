from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class BooksQuotesUserManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an Email Address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not other_fields.get('is_staff'):
            raise ValueError("SuperUser must have assigned is_staff=True")
        if not other_fields.get('is_superuser'):
            raise ValueError("SuperUser must have assigned is_superuser=True")

        user = self.model(
            email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save()
        return user


class BooksQuotesUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=125)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = BooksQuotesUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]


    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        verbose_name = "User"
