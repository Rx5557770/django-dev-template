from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    ]
    search_fields = ["username", "email"]
    list_filter = ["is_active"]
    list_per_page = 20
    list_editable = ["is_staff", "is_active"]
