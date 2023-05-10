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

                #Check if employees with the given ID already exists
                if Employee.objects.filter(id_number=id_number).exists():
                        messages.error(request, 'ID Already Exists')
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
        #to find the Employee object with the primary key equals to pk and delete the object from database
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
                #payroll_pk = Employee.objects.get(pk=payroll_for)
                #payroll_rate = payroll_pk.rate
                #payroll_allowance = payroll_pk.allowance
                #payroll_overtime = payroll_pk.overtime_pay
                month = request.POST.get('month')
                year = request.POST.get('year')
                cycle = request.POST.get('cycle') #Make if statements and do the math with variables of payslips and employees

                if cycle == '1':
                        pay_cycle = 1
                        date_range = '1-15'
                        pag_ibig_rate = 100
                else:
                        pay_cycle = 2
                        date_range = '16-30'
                        philhealth_rate = 0.04
                        sss_rate = 0.045
                
                if payroll_for =='all_employees':
                       selected_employees = employees
                else:
                       selected_employee = get_object_or_404(Employee, pk=payroll_for)
                       selected_employees = [selected_employee]

                for employee in selected_employees:
                       payslip_exists = Payslip.objects.filter(id_number=employee, month=month, year=year, pay_cycle=cycle).exists()
                       if payslip_exists:
                                messages.error(request, f"Payslip already exists for Employee ID: {employee.id_number}")
                       else:
                                payroll_rate = employee.rate
                                payroll_allowance = employee.allowance
                                payroll_overtime = employee.overtime_pay

                                if cycle == '1':
                                        tax_rate = 0.2
                                        tax = ((payroll_rate / 2) + payroll_allowance + payroll_overtime - pag_ibig_rate) * tax_rate
                                        total_pay_Wtax = ((payroll_rate / 2) + payroll_allowance + payroll_overtime - pag_ibig_rate) - tax
                                        payslip_context = {
                                                'id_number': employee,
                                                'month': month,
                                                'date_range': date_range,
                                                'year': year,
                                                'pay_cycle': pay_cycle,
                                                'rate': payroll_rate,
                                                'earnings_allowance': payroll_allowance,
                                                'deductions_tax': tax,
                                                'overtime': payroll_overtime,
                                                'total_pay': total_pay_Wtax,
                                                'pag_ibig': pag_ibig_rate,
                                        }
                                else:
                                        tax_rate = 0.2
                                        philhealth = payroll_rate * philhealth_rate
                                        sss = payroll_rate * sss_rate
                                        tax = ((payroll_rate / 2) + payroll_allowance + payroll_overtime - philhealth - sss) * tax_rate
                                        total_pay_Wtax = ((payroll_rate / 2) + payroll_allowance + payroll_overtime - philhealth - sss) - tax
                                        payslip_context = {
                                                'id_number': employee,
                                                'month': month,
                                                'date_range': date_range,
                                                'year': year,
                                                'pay_cycle': pay_cycle,
                                                'rate': payroll_rate,
                                                'earnings_allowance': payroll_allowance,
                                                'deductions_tax': tax,
                                                'deductions_health': philhealth,
                                                'overtime': payroll_overtime,
                                                'total_pay': total_pay_Wtax,
                                                'sss': sss,
                                        }
                                Payslip.objects.create(**payslip_context)
                                employee.resetOvertime()

                                messages.success(request, f"Payslips created successfully for Employee ID: {employee.id_number}")

                
                return redirect('payslips')

        return render(request, 'payroll_app/payslips.html', {'employees':employees, 'payslips':payslips})

def view_payslips(request, pk):
        #retrieves single Payslip object using its primary key
        payslips = get_object_or_404(Payslip, pk=pk)
        return render(request, 'payroll_app/view_payslips.html', {'payslips':payslips})
