from django.contrib import admin
from .models import UserAddress
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ContactMessage, Doctor


# Register your models here.
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street_address", "city", "state", "country", "postal_code", "is_default")
    list_filter = ("city", "state", "country", "is_default")
    search_fields = ("user__email", "user__username", "street_address", "city", "state", "country", "postal_code")
    ordering = ("user", "country", "state", "city")
    list_editable = ("is_default",)
    list_per_page = 25

    fieldsets = (
        ("User Details", {"fields": ("user",)}),
        ("Address Information", {"fields": ("houseNo","street_address", "city", "state", "country", "postal_code")}),
        ("Settings", {"fields": ("is_default",)}),
    )

    # Optional: Prevent marking multiple addresses as default
    def save_model(self, request, obj, form, change):
        if obj.is_default:
            UserAddress.objects.filter(user=obj.user).update(is_default=False)
        super().save_model(request, obj, form, change)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')  # Fields to show in list view
    list_filter = ('user_type', 'is_staff', 'is_active')  # Filters on the right
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'user_gender', 'first_name', 'last_name', 'profile_image', 'date_of_birth', 'phone_number')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "message")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'consultation_fee', 'is_active')
    list_filter = ('specialization', 'experience', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    ordering = ('user__first_name',)
