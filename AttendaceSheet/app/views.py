from django.shortcuts import render
import csv
from rest_framework import status
from .models import EmployeeAttendance
from .serializers import EmployeeAttendanceSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
# Create your views here.

class EmployeeAttendanceView(APIView):
    def get(self,request):
        try:
            attendance_mapping={
                'P':'Present',
                'A':'Absent',
                'L':'Leave'
            }
            attendance_data=[]
            with open('attendance.csv','r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # print(csv_reader)
                for row in csv_reader:
                    # print(row)
                    row['attendance'] = attendance_mapping.get(row['attendance'], 'Unknown')  # Fix the typo here
                    attendance_data.append(row)
            
             # Calculate the number of absent days for each employee
            absent_days = {}
            for record in attendance_data:
                if record['attendance'] == 'Absent':
                    employee_name = record['E.mail']
                    absent_days[employee_name] = absent_days.get(employee_name, 0) + 1
            # print(absent_days)
            
             # Generate email templates using Handlebars
            email_templates = []
            for employee, days in absent_days.items():
                email_template = f"Hi {employee},\n" \
                                 f"This email is to inform you that according to our attendance records, you are absent from your duties for {days} days. Please apply for leave.\n" \
                                 f"Thanks,\nHR Team"
                email_templates.append(email_template)
            
            # Send emails to absent candidates with 2 or more days of absence
            for employee, days in absent_days.items():
                print(employee,days)
                if days >= 2:
                    candidate_data = next((row for row in attendance_data if row['e.name'] == employee), None)
                    if candidate_data:
                        candidate_email_template = f"Hi {employee},\n" \
                                        f"This email is to inform you that according to our attendance records, you are absent from your duties for {days} days. Please apply for leave.\n" \
                                        f"Thanks,\nHR Team"
                        
                        # Email template for employer
                        employer_email_template = f"Hello Employer,\n" \
                                                 f"This is to inform you that {employee} has been absent from their duties for {days} days according to our attendance records. Please take appropriate action.\n" \
                                                 f"Thanks,\nHR Team"
                        

                            # Send email to candidate
                        send_mail(
                            subject='Absents Notice',
                            message=candidate_email_template,
                            from_email='cccccccc@gmail.com',
                            recipient_list=[candidate_data['E.mail']],  # Use the correct key for email
                        )

                        # Send email to employer
                        send_mail(
                            subject=f'Absents Report: {employee}',
                            message=employer_email_template,
                            from_email='XXXXXXXX@gmail.com',
                            recipient_list=['XXXXXXXX@gmail.com'],  # Replace with the employer's email
                        )

            return Response({'message':'Emails sent to absent candidates..'})
        except Exception as e:
            # print(str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self,request):
        try:
            serializer=EmployeeAttendanceSerializers(data=request.data,many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

