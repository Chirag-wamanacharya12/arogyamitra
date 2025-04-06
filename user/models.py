from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a user with an email, username, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ("patient", "Patient"),
        ("physician", "Physician"),
        ("practitioner", "Practitioner"),
        ("researcher", "Researcher"),
        ("service_provider", "Service Provider"),
        ("health_creator", "Health Content Creator"),
        ("guest", "Guest"),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="guest")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(null=True,blank=True)
    user_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Other')
    
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Boolean flags to indicate whether the user is active
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # staff user
    is_superuser = models.BooleanField(default=False)  # superuser

    # Required fields
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'  # Email is the unique identifier

    # Custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    houseNo = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)  # Mark one address as default
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"
    
class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=100, help_text="e.g., Monday, Wednesday, Friday")
    start_time = models.TimeField(help_text="Available from (HH:MM)")
    end_time = models.TimeField(help_text="Available until (HH:MM)")
    is_active = models.BooleanField(default=True, help_text="Set to False if the doctor is unavailable")

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
