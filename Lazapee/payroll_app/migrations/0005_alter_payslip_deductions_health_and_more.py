# Generated by Django 4.1.7 on 2023-04-30 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0004_alter_payslip_pag_ibig_alter_payslip_sss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='deductions_health',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='deductions_tax',
            field=models.FloatField(default=0),
        ),
    ]
