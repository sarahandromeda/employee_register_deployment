from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'test1@super.com', 
            'superuser1', 
            'Joe',
            'Bob', 
            'password'
        )
        self.assertEqual(super_user.email, 'test1@super.com')
        self.assertEqual(super_user.user_name, 'superuser1')
        self.assertEqual(super_user.first_name, 'Joe')
        self.assertEqual(super_user.last_name, 'Bob')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'superuser1')

        with self.assertRaises(ValidationError):
            db.objects.create_superuser(
                'test3@super.com', 
                'superuser3', 
                'Joe',
                'Bob', 
                'password',
                is_superuser= False
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'test1@user.com', 
            'user1', 
            'Joe',
            'Bob', 
            'password'
        )
        self.assertEqual(user.email, 'test1@user.com')
        self.assertEqual(user.user_name, 'user1')
        self.assertEqual(user.first_name, 'Joe')
        self.assertEqual(user.last_name, 'Bob')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'user1')

        with self.assertRaises(ValidationError):
            db.objects.create_user(
                email = "",
                user_name = 'user2', 
                first_name = 'Joe',
                last_name = 'Bob', 
                password = 'password'
            )



 
