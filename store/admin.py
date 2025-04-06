from django.contrib import admin
from .models import PrimaryCategory, SubCategory, fullBanner, ProductBase, Formulation, Tray
from .models import ProductImage, PricingDetails, Order, Cart, ImportantInfo, ProductReview, processedtocheck

@admin.register(PrimaryCategory)
class PrimaryCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_Name', 'cat_Desc','is_ageRestricted')
    search_fields = ('cat_Name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'primary_category', 'description')
    search_fields = ('name',)

@admin.register(fullBanner)
class FullBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'brandName')
    search_fields = ('brandName',)

@admin.register(ProductBase)
class ProductBaseAdmin(admin.ModelAdmin):
    list_display = ('name','brand_name', 'rating', 'quantity', 'item_code', 'stock_quantity', 'is_active', 'formulation', 'barcode')
    search_fields = ('title', 'brand_name', 'item_code', 'barcode')
    list_filter = ('brand_name', 'is_active', 'formulation')
    ordering = ('-total_purchased',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product__title', 'product__brand_name')

@admin.register(PricingDetails)
class PricingDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'offer', 'ends_in')
    search_fields = ('name', 'product__brand_name')
    list_filter = ('offer',)


@admin.register(Formulation)
class FormulationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tray)
class TrayAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_checked_out')
    search_fields = ('user__username',)
    list_filter = ('is_checked_out', 'expires_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('checkedToProceed','uid', 'product','Pricing', 'prodImage', 'savedForLater', 'qty')
    search_fields = ('uid__username', 'pid__title')
    list_filter = ('savedForLater',)

@admin.register(ImportantInfo)
class ImportantInfoAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product__title', 'product__brand_name')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__title', 'user')
    list_filter = ('rating', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'order_status', 'ordered_at', 'updated_at')
    list_filter = ('order_status', 'ordered_at', 'updated_at')
    search_fields = ('user__username', 'product__name', 'order_status')
    ordering = ('-ordered_at',)
    readonly_fields = ('ordered_at', 'updated_at')

    fieldsets = (
        ('Order Details', {
            'fields': ('user', 'product', 'Pricing', 'quantity', 'total_price')
        }),
        ('Status & Timestamps', {
            'fields': ('order_status', 'ordered_at', 'updated_at')
        }),
    )


@admin.register(processedtocheck)
class ProcessedToCheckAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'email', 'phone_number', 'city', 'pin_code')
    list_filter = ('city', 'country')
    search_fields = ('full_name', 'email', 'phone_number', 'address', 'city')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'email', 'phone_number')
        }),
        ('Address Details', {
            'fields': ('address', 'city', 'pin_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('additional_notes',),
            'classes': ('collapse',)
        })
    )