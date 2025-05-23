# Generated by Django 5.1.5 on 2025-03-15 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('specialization', models.CharField(max_length=255)),
                ('clinic_address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('hospital_affiliation', models.CharField(blank=True, max_length=255, null=True)),
                ('years_of_experience', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
