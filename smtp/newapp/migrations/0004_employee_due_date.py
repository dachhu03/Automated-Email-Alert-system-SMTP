# Generated by Django 5.1.6 on 2025-02-18 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0003_alter_employee_reg_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
