from django.contrib import admin
from .models import Employee, Payslip
# Register your models here.
# Register created models here in order to update objects with admin power

admin.site.register(Employee)
admin.site.register(Payslip)