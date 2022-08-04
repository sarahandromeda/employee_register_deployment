from django.test import TestCase
from django.contrib.auth import get_user_model
from user_register.models import NewUser
from main_register.models import Employee

# Create your tests here.

class NewCompanyTests(TestCase):
    pass

class NewDepartmentTests(TestCase):
    pass

class NewEmployeeTests(TestCase):
    def test_creation(self):
        db = get_user_model()
        user = db.objects.create_user(
            'test1@user.com', 
            'user1', 
            'Joe',
            'Bob', 
            'password'
        )
        employee = Employee.objects.create(
            email = 'a@a.com',
            first_name = 'John',
            last_name = 'Doe',
            phone_number = '1234567890',
            title = 'Tech',
            is_supervisor = False,
            user = user,
        )

        self.assertEqual(employee.email, 'a@a.com')
        self.assertEqual(employee.first_name, 'John')
        self.assertEqual(employee.last_name, 'Doe')
        self.assertEqual(employee.phone_number, '1234567890')
        self.assertEqual(employee.title, 'Tech')
        self.assertFalse(employee.is_supervisor)