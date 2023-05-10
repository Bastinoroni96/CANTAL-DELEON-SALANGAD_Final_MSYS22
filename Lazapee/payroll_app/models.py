from django.db import models

#hello
# Create your models here.
# Employee model, when objects are created, ID numbers have to be unique
class Employee(models.Model):
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20, unique=True)
    rate = models.FloatField()
    overtime_pay = models.FloatField(default=0, blank = True)
    allowance = models.FloatField(null = True, blank = True)

# This is an Employee model representing an employee's information
    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        return self.overtime_pay
    
    def resetOvertime(self):
        self.overtime_pay = 0
        self.save()

    def getAllowance(self):
        return self.allowance
    
    def __str__(self):
        return f"{self.id_number}"
    

class Payslip(models.Model):
    id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=50)
    date_range = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    pay_cycle = models.IntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField()
    deductions_tax = models.FloatField(default=0)
    deductions_health = models.FloatField(default=0)
    pag_ibig = models.FloatField(default=100)
    sss = models.FloatField(default=0.045)
    overtime = models.FloatField()
    total_pay = models.FloatField()

# This is a Payslip model representing an employee's payslip information 
    def IDNumber(self):
        return self.id_number
    
    def getMonth(self):
        return self.month
    
    def getDate_range(self):
        return self.date_range
    
    def getYear(self):
        return self.year
    
    def getPay_cycle(self):
        return self.pay_cycle
    
    def getRate(self):
        return self.rate
    
    def getCycleRate(self):
        return self.rate / 2
    
    def getEarnings_allowance(self):
        return self.earnings_allowance
    
    def getDeductions_tax(self):
        return self.deductions_tax
    
    def getDeductions_health(self):
        return self.deductions_health
    
    def getPag_ibig(self):
        return self.pag_ibig
    
    def getSSS(self):
        return self.sss
    
    def getOvertime(self):
        return self.overtime
    
    def getTotal_pay(self):
        return self.total_pay
    
    def __str__(self):
        return f"pk: {self.pk}, Employee: {self.id_number}, Period: {self.month} {self.date_range}, {self.year}, Cycle: {self.pay_cycle}, Total Pay: {self.total_pay}"



