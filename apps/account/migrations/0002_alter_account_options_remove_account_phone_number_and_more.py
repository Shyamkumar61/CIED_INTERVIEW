# Generated by Django 5.1.3 on 2025-03-16 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="account",
            options={"verbose_name": "Account", "verbose_name_plural": "Accounts"},
        ),
        migrations.RemoveField(
            model_name="account",
            name="phone_number",
        ),
        migrations.AlterField(
            model_name="account",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("med_staff", "Medical Staff"),
                    ("inventory_manager", "Inventory Manager"),
                ],
                default="admin",
                max_length=20,
                verbose_name="Role",
            ),
        ),
    ]
