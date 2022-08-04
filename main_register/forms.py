from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms 
from main_register.models import Employee, Department, Company

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']
        help_texts = {
            'phone_number': _("Formats: 123-456-7890 or (123)456-7890 May also prefix with country code."),
        }

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        exclude = ['user', 'employees', 'department_head']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ['user', 'departments']

class EditDepartmentForm(ModelForm):
    class Meta:
        model = Department
        exclude = ['user', 'employees']