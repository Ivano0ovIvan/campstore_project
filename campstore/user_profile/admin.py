from django.contrib import admin
from .models import UserProfileModel


@admin.register(UserProfileModel)
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "is_seller")
    search_fields = ("first_name", 'last_name')
    list_filter = ("is_seller",)
    ordering = ("first_name", "last_name",)
