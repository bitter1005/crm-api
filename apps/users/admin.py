from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomsUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Роль", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_staff")


# Register your models here.
