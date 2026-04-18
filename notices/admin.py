from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view [cite: 26]
    list_display = ('title', 'category', 'posted_date', 'expiry_date', 'is_important')
    list_filter = ('category', 'is_important', 'author')
    search_fields = ('title', 'body', 'author__username', 'author__first_name', 'author__last_name')