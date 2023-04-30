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

def payslips(request):
        employees = Employee.objects.all()
        payslips = Payslip.objects.all()
        if(request.method=="POST"):
                payroll_for = request.POST.get('payroll_for')
                payroll_pk = Employee.objects.get(pk=payroll_for)
                payroll_rate = payroll_pk.rate
                payroll_allowance = payroll_pk.allowance
                payroll_overtime = payroll_pk.overtime_pay
                month = request.POST.get('month')
                year = request.POST.get('year')
                cycle = request.POST.get('cycle') #Make if statements and do the math with variables of payslips and employees

                if cycle == '1':
                        pay_cycle1 = 1
                        date_range1 = '1-15'
                        pag_ibig = 100
                        tax1 = ((payroll_rate/2) + payroll_allowance + payroll_overtime - pag_ibig)*0.2
                        total_pay_Wtax1 = ((payroll_rate/2) + payroll_allowance + payroll_overtime - pag_ibig)-tax1
                        Payslip.objects.create(id_number=payroll_pk, month=month, date_range=date_range1, year=year, pay_cycle=pay_cycle1, rate=payroll_rate, earnings_allowance=payroll_allowance, deductions_tax=tax1, overtime=payroll_overtime, total_pay=total_pay_Wtax1, pag_ibig=pag_ibig)
                        employee = Employee.objects.get(pk=payroll_for)
                        employee.resetOvertime()
                        return redirect('payslips')



                if cycle == '2':
                        pay_cycle2 = 2
                        date_range2 = '16-30'
                        philhealth = payroll_pk.rate*0.04
                        sss = payroll_pk.rate*0.045
                        tax2 = ((payroll_rate/2) + payroll_allowance + payroll_overtime - philhealth - sss)*0.2
                        total_pay_Wtax2 = ((payroll_rate/2) + payroll_allowance + payroll_overtime - philhealth - sss)-tax2
                        Payslip.objects.create(id_number=payroll_pk, month=month, date_range=date_range2, year=year, pay_cycle=pay_cycle2, rate=payroll_rate, earnings_allowance=payroll_allowance, deductions_health=tax2, overtime=payroll_overtime, total_pay=total_pay_Wtax2, sss=sss)
                        employee = Employee.objects.get(pk=payroll_for)
                        employee.resetOvertime()
                        return redirect('payslips')

        return render(request, 'payroll_app/payslips.html', {'employees':employees, 'payslips':payslips})
