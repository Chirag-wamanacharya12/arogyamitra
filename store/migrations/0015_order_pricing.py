# Generated by Django 5.1.5 on 2025-03-08 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_cart_checkedtoproceed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Pricing',
            field=models.ForeignKey(db_column='pricing_id', default=None, on_delete=django.db.models.deletion.CASCADE, to='store.pricingdetails'),
        ),
    ]
