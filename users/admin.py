from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

# rejestracja CustomUser w django admin
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, 
         {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2"),
        }),
    )
    list_display = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)