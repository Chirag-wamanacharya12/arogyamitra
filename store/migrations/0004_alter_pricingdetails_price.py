# Generated by Django 5.1.5 on 2025-03-07 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productbase_primarycategory_productbase_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricingdetails',
            name='price',
            field=models.CharField(max_length=70),
        ),
    ]
