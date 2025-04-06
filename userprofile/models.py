from django.db import models
from user.models import CustomUser
from datetime import date

class Medication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=255)  # Medication name
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 2 tablets")  
    frequency = models.CharField(max_length=100, help_text="e.g., Twice a day, Once daily")  
    start_date = models.DateField()
    end_date = models.DateField()
    refill_reminder = models.BooleanField(default=True)  # Enable refill reminders
    refill_date = models.DateField(blank=True, null=True)  # Date when refill is due
    notes = models.TextField(blank=True, null=True)  # Optional notes

    def is_expiring_soon(self):
        """Returns True if the medication is expiring within 7 days."""
        return (self.end_date - date.today()).days <= 7

    def __str__(self):
        return f"{self.name} - {self.dosage} ({self.user.username})"

class FamilyDoctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="FamilyDoctor")
    full_name = models.CharField(max_length=255)
    profileImage = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=255)
    clinic_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"

class PatientVital(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="PatientVital")
    birth_date = models.DateField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    
    blood_pressure_systolic = models.IntegerField()  # e.g., 120
    blood_pressure_diastolic = models.IntegerField()  # e.g., 89
    heart_rate = models.IntegerField()  # e.g., 120 BPM
    glucose = models.FloatField()  # e.g., 97 mg/dL
    cholesterol = models.FloatField()  # e.g., 85 mg/dL
    weight = models.FloatField(default=1)  # e.g., 70 kg
    height = models.FloatField(default=1)  # e.g., 170 cm
    recorded_at = models.DateTimeField(auto_now_add=True)


    def bmi(self):
        if self.weight and self.height:
            return round(self.weight / (self.height / 100) ** 2, 2)

    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return f"{self.blood_group}"

class HealthDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="health_documents")
    title = models.CharField(max_length=255)  # Document name
    document = models.FileField(upload_to="health_documents/")  # Upload location
    description = models.TextField(blank=True, null=True)  # Optional notes
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class FamilyMember(models.Model):
    RELATIONSHIP_CHOICES = [
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="family_members")
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15, blank=True)  # contact field

    def __str__(self):
        return f"{self.name} ({self.relationship})"
