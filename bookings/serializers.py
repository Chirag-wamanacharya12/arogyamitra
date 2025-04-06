from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = '__all__'

    def get_title(self, obj):
        return f"Dr. {obj.doctor.user.username} - {obj.appointment_type.capitalize()}"

    def get_start(self, obj):
        return f"{obj.appointment_date}T{obj.appointment_time}"

    def get_end(self, obj):
        return f"{obj.appointment_date}T{obj.appointment_time}"  # Adjust if needed

    def get_color(self, obj):
        return "#007bff" if obj.status == "confirmed" else "#ffc107"
