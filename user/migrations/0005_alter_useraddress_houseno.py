# Generated by Django 5.1.5 on 2025-03-11 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_useraddress_houseno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='houseNo',
            field=models.CharField(max_length=255),
        ),
    ]
