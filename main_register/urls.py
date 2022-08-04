from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/', views.user_home, name= 'user_home'),
    path('<int:company>/', views.department_page, name='department_page'),
    path('<int:company>/<int:department>/', views.employee_page, name='employee_page'),
    path('company/<int:company_id>/', views.company_edit, name="company_edit"),
    path('department/<int:department_id>/', views.department_edit, name="department_edit"),
    path('employee/<int:employee_id>/', views.employee_edit, name="employee_edit"),
]