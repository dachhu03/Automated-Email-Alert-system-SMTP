# Generated by Django 5.1.6 on 2025-02-18 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0002_employee_reg_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='reg_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
