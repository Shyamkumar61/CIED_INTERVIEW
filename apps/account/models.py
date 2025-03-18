from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import AccountManager

# Create your models here.


class Account(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("med_staff", "Medical Staff"),
        ("inventory_manager", "Inventory Manager"),
    )

    email = models.EmailField(unique=True, verbose_name="Email Address", max_length=254)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="admin", verbose_name="Role"
    )

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
