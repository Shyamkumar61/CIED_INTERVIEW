# Generated by Django 5.1.3 on 2025-03-18 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_medicine_expiry_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medicine",
            name="threshold",
        ),
        migrations.AlterField(
            model_name="medicine",
            name="stock_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
