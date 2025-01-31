from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(models.CustomUser)
admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Hospital)

