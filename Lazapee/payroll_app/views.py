from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Payslip 


# Create your views here.
def view_employee(request):
        employee_objects = Employee.objects.all()
        return render(request, 'payroll_app/view_employee.html',{'employees':employee_objects})

def create_employee(request):
        if(request.method=="POST"):
                name = request.POST.get('name')
                id_number = request.POST.get('id')
                rate = request.POST.get('rate')

                if not name:
                        messages.error(request, 'Please enter a name')
                        return redirect('create_employee')
                if not id_number:
                        messages.error(request, 'Please enter an ID number')
                        return redirect('create_employee')
                if not rate:
                        messages.error(request, 'Please enter a rate')
                        return redirect('create_employee')

                if name and id_number and rate:
                        allowance = request.POST.get('allowance') or 0.0
                        Employee.objects.create(name=name, id_number=id_number, rate=rate, allowance=allowance)
                        messages.success(request, 'Employee created successfully')
                        return redirect('view_employee')
        else:
                return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
        if(request.method=="POST"):
                name = request.POST.get('name')
                id_number = request.POST.get('id')
                rate = request.POST.get('rate')

                if not name:
                        messages.error(request, 'Please enter a name')
                        return redirect('create_employee')
                if not id_number:
                        messages.error(request, 'Please enter an ID number')
                        return redirect('create_employee')
                if not rate:
                        messages.error(request, 'Please enter a rate')
                        return redirect('create_employee')

                if name and id_number and rate:
                        allowance = request.POST.get('allowance') or 0.0
                        Employee.objects.filter(pk=pk).update(name=name, id_number=id_number, rate=rate, allowance=allowance)
                        return redirect('view_employee')
        else:
                e = get_object_or_404(Employee, pk=pk)
                return render(request, 'payroll_app/update_employee.html', {'e':e})

def delete_employee(request, pk):
        Employee.objects.filter(pk=pk).delete()
        return redirect('view_employee')

def calculate_overtimepay(request, pk):
        if(request.method=="POST"):
                employee = get_object_or_404(Employee, pk=pk)
                overtime_hours = request.POST.get('overtime_hours') or 0.0
                rate = employee.rate
                overtime_pay_value = (rate / 160) * 1.5 * float(overtime_hours)
                Employee.objects.filter(pk=pk).update(overtime_pay=overtime_pay_value)
                return redirect('view_employee')
        
        return redirect('view_employee')
