from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["username"]
    date_hierarchy = "created_at"
    ordering = ["username"]
    show_facets = admin.ShowFacets.ALWAYS
