# Generated by Django 5.1.5 on 2025-03-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbase',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productbase',
            name='is_prescription_required',
            field=models.BooleanField(default=False),
        ),
    ]
