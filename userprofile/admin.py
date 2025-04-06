from django.contrib import admin
from .models import Medication, FamilyDoctor, PatientVital, FamilyMember

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "dosage", "frequency", "start_date", "end_date", "refill_reminder")
    list_filter = ("refill_reminder", "end_date")
    search_fields = ("user__email", "name")
    ordering = ("end_date",)


@admin.register(FamilyDoctor)
class FamilyDoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'specialization', 'phone', 'email', 'city', 'state', 'years_of_experience', 'is_active')
    search_fields = ('full_name', 'phone', 'email', 'specialization', 'hospital_affiliation')
    list_filter = ('specialization', 'city', 'state', 'is_active')
    ordering = ('full_name',)

@admin.register(PatientVital)
class PatientVitalAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'blood_group', 'blood_pressure_systolic', 
                    'blood_pressure_diastolic', 'heart_rate', 'glucose', 'cholesterol', 'recorded_at')
    list_filter = ('blood_group', 'recorded_at')
    search_fields = ('user', 'blood_group')
    ordering = ('-recorded_at',)
    readonly_fields = ('age', 'recorded_at')  # Age is dynamically calculated

    def age(self, obj):
        return obj.age()
    age.short_description = 'Age'  # Rename column in the admin panel

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "relationship", "date_of_birth", "gender", "contact_number")
    search_fields = ("name", "user__email", "relationship", "contact_number")
    list_filter = ("relationship", "gender")
    ordering = ("user", "name")
