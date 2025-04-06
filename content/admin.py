from django.contrib import admin
from .models import LongFormVideo, ShortVideo

@admin.register(LongFormVideo)
class LongFormVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'upload_date', 'views')
    search_fields = ('title', 'uploader__username')
    list_filter = ('upload_date', 'category')

@admin.register(ShortVideo)
class ShortVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'upload_date', 'views', 'is_trending')
    search_fields = ('title', 'uploader__username', 'hashtags')
    list_filter = ('upload_date', 'is_trending')
