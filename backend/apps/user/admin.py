
from django.contrib import admin

from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', )
    fields = ('username', 'first_name', 'language',
              'last_name', 'email', 'is_active', 'date_joined', 'is_staff')

    readonly_fields = ('date_joined',)

    search_fields = ('phone_number',)
