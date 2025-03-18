from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.


@admin.register(Account)
class AccountAdmin(UserAdmin):

    model = Account
    list_display = ("username", "email", "first_name", "last_name", "role")
    fieldsets = UserAdmin.fieldsets + (("Roles", {"fields": ("role",)}),)
