from django.db import models
from datetime import datetime

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=50)
    phone = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=50, null=True, blank=True)  # Allows NULL values
    due_date = models.DateField(null=True, blank=True)
    service_status = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name