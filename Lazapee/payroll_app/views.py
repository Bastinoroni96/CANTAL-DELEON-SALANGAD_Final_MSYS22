from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Payslip 


# Create your views here.
def view_employee(request):
        employee_objects = Employee.objects.all()
        return render(request, 'payroll_app/view_employee.html',{'employees':employee_objects})

def create_employee(request):
        return render(request, 'payroll_app/create_employee.html')
