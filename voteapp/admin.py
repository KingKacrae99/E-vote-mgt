from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class MemberAdmin(UserAdmin):
    model = Member
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    ordering = ('phone',)

# Register your models here.

admin.site.register(Member, MemberAdmin)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
