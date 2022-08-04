from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class Employee(models.Model):
    email = models.EmailField(_('email address'))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=17)
    start_date = models.DateField()
    title = models.CharField(max_length=150)
    is_supervisor = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

            
class Department(models.Model):
    name = models.CharField(max_length=150)
    employees = models.ManyToManyField(Employee)
    department_head = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='department_head', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=150)
    industry = models.CharField(max_length=100)
    departments = models.ManyToManyField(Department)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

