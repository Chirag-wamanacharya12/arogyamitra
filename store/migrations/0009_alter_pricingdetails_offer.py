# Generated by Django 5.1.5 on 2025-03-08 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_pricingdetails_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingdetails',
            name='offer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
