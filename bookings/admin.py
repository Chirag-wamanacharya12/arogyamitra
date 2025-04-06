from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'preferred_time_slot', 'status', 'payment_status')
    list_filter = ('appointment_date', 'status', 'payment_status')
    search_fields = ('patient__username', 'doctor__user__username', 'appointment_date')
    ordering = ('appointment_date', 'preferred_time_slot')
