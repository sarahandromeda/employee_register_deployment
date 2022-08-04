from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main_register.models import Employee, Department, Company
from main_register.forms import EmployeeForm, DepartmentForm, CompanyForm, EditDepartmentForm

# Create your views here.

# Function to determine ajax request
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def home(response):
    return render(response, 'main_register/home.html', {})

@login_required
def user_home(response):
    user = response.user
    companies = user.company_set.all()
    company_form = CompanyForm()
    if response.method == 'POST':
        company_form = CompanyForm(response.POST)
        if company_form.is_valid():
            form = company_form.save(commit=False)
            form.user = user
            form.save()

            return redirect('user_home')

    values_dict = {
        'user': user, 
        'companies' : companies, 
        'company_form': company_form
        }
    return render(
        response, 
        'main_register/user_home.html', 
        values_dict
        )

@login_required
def department_page(response, company):
    user = response.user
    company = user.company_set.get(id=company)
    departments = company.departments.all()

    department_form = DepartmentForm()
    if response.method == 'POST':
        department_form = DepartmentForm(response.POST)
        if department_form.is_valid():
            company.departments.create(
                name = department_form.cleaned_data['name'],
                user = user,
            )

            return redirect('department_page', company=company.id)

    values_dict = {
        'user': user, 
        'departments': departments, 
        'company': company, 
        'department_form': department_form
        }
    return render(
        response, 
        'main_register/department_page.html',
        values_dict
        )


@login_required
def employee_page(response, company, department):
    user = response.user
    employee_form = EmployeeForm()
    department = user.department_set.get(id=department)
    employees = department.employees.all()

    if response.method == 'POST':
        employee_form = EmployeeForm(response.POST)
        if employee_form.is_valid():
            data = employee_form.cleaned_data
            # must use create to add object to related set
            department.employees.create(
                email = data['email'],
                first_name = data['first_name'],
                last_name = data['last_name'],
                phone_number = data['phone_number'],
                start_date = data['start_date'],
                title = data['title'],
                is_supervisor = data['is_supervisor'],
                user = user
            )
            return redirect(
                'employee_page', 
                company = company, 
                department = department.id,
                )

    values_dict = {
        'user': user,
        'employees': employees,
        'employee_form': employee_form,
        'department': department,
        'company_id' : company
        }
    return render(response, 'main_register/employee_page.html',values_dict)

@login_required
def company_edit(response, company_id):
    company = Company.objects.get(id=company_id)
    company_edit_form = CompanyForm(instance=company)
    if response.method == 'POST':
        if response.POST.get('update'):
            company_edit_form = CompanyForm(response.POST, instance=company)
            if company_edit_form.is_valid():
                company_edit_form.save()
                return redirect('department_page', company= company.id)
        elif response.POST.get('delete'):
            company.delete()
            # must redirect to parent page of specific company as company no longer exists
            return redirect('user_home')

    values_dict = {
        'company_edit_form': company_edit_form,
        'company': company,
    }
    return render(response, 'main_register/company_edit.html', values_dict)

@login_required
def department_edit(response, department_id):
    department = Department.objects.get(id=department_id)
    department_edit_form = EditDepartmentForm(instance=department)
    department_edit_form.fields['department_head'].queryset = department.employees.all()
    if response.method == 'POST':
        if response.POST.get('update'):
            department_edit_form = EditDepartmentForm(response.POST, instance=department)
            if department_edit_form.is_valid():
                department_edit_form.save()
                # get company id for redirect
                company = department.company_set.all()[0]
                return redirect(
                    'employee_page',
                    company = company.id,
                    department = department.id
                    )
        elif response.POST.get('delete'):
            # get parent company before deleting for redirect
            company = department.company_set.all()[0]
            department.delete()
            # redirect to parent page of list of departments
            return redirect('department_page', company=company.id)

    values_dict = {
        'department_edit_form': department_edit_form,
        'department': department,
    }
    return render(response, 'main_register/department_edit.html', values_dict)


@login_required
def employee_edit(response, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee_edit_form = EmployeeForm(instance=employee)
    
    if response.method == 'POST':
        if response.POST.get('update'):
            employee_edit_form = EmployeeForm(response.POST, instance=employee)
            if employee_edit_form.is_valid():
                employee_edit_form.save()
                # get department and company parents for redirect
                department = employee.department_set.all()[0]
                company = department.company_set.all()[0]
                return redirect(
                    'employee_page', 
                    company = company.id, 
                    department = department.id,
                    )
        elif response.POST.get('delete'):
            # get parent company and department before delete
            department = employee.department_set.all()[0]
            company = department.company_set.all()[0]
            employee.delete()
            return redirect(
                'employee_page', 
                company = company.id, 
                department = department.id
                )

    values_dict = {
        'employee_edit_form': employee_edit_form,
        'employee': employee,
    }        
    return render(response, 'main_register/employee_edit.html', values_dict)