from rest_framework import serializers
from . models import EmployeeAttendance

class EmployeeAttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'