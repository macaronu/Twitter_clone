from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjUserAdmin
from .models import User
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
class UserAdmin(DjUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('date_of_birth', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)