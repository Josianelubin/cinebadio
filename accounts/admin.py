from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "cree_le")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-cree_le",)
    fieldsets = UserAdmin.fieldsets + (
        ("Informations CinéBadio", {"fields": ("avatar", "bio", "date_naissance", "notifications_email")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations CinéBadio", {"fields": ("email", "avatar", "bio")}),
    )
