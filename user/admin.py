from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile
# Register your models here.


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'email', 'phone')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class ProfileInline(admin.StackedInline):
    model = Profile


class ExtendedUserAdmin(CustomUserAdmin):
    inlines = CustomUserAdmin.inlines + [ProfileInline]


admin.site.register(CustomUser, ExtendedUserAdmin)
