from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'is_verified')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
