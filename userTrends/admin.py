from django.contrib import admin
from .models import ClickedProduct

# Register your models here.
@admin.register(ClickedProduct)
class ClickedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'price', 'clicked_at')
    list_filter = ('clicked_at', 'user')
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'clicked_at'
    readonly_fields = ('clicked_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Product Details', {
            'fields': ('product', 'price', 'image', 'info', 'review')
        }),
        ('Timestamp', {
            'fields': ('clicked_at',)
        }),
    )