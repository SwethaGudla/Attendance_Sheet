from django.db import models

class EmployeeAttendance(models.Model):
    e_code = models.PositiveIntegerField()
    e_name = models.CharField(max_length=100)
    date = models.DateField()
    attendance = models.CharField(max_length=1, choices=[
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave')
    ])
    e_email = models.EmailField()

