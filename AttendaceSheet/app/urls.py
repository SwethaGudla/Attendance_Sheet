from django.urls import path
from app.views import EmployeeAttendanceView

urlpatterns=[
    path('attendance/',EmployeeAttendanceView.as_view(),name='attendance'),
]