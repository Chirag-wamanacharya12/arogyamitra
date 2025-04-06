from django.db import models
from user.models import CustomUser
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
User = get_user_model()

VIDEO_EXTENSIONS = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']

class LongFormVideo(models.Model):
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='long_videos/',
        validators=[FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)]
    )
    thumbnail = models.ImageField(upload_to='thumbnails/long/', blank=True, null=True)
    duration = models.DurationField()
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, choices=[
        ("Education", "Education"),
        ("Entertainment", "Entertainment"),
        ("News", "News"),
        ("Sports", "Sports"),
        ("Music", "Music"),
        ("Gaming", "Gaming"),
        ("Other", "Other"),
    ])

    def save(self, *args, **kwargs):
        if self.duration.total_seconds() <= 60:
            raise ValueError("Long-form videos must be longer than 60 seconds")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"🎥 {self.title} by {self.uploader}"

class ShortVideo(models.Model):
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False) # Get the logged-in user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='short_videos/',
        validators=[FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)]
    )
    thumbnail = models.ImageField(upload_to='thumbnails/shorts/', blank=True, null=True)
    duration = models.DurationField()
    views = models.PositiveIntegerField(default=0)
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    is_trending = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.duration.total_seconds() > 60:
            raise ValueError("Short videos must be 60 seconds or less")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"📱 {self.title} by {self.uploader}"

