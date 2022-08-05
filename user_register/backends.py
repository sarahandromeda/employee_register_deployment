from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from .models import NewUser

class CustomBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            # see if email is in database
            user = NewUser.objects.get(email=email)
            if check_password(password, user.password):
                return user
            else:
                raise ValidationError('Password is incorrect.')
                return None

        except NewUser.DoesNotExist:
            raise ValidationError('No account found with that email.')
            return None

    def get_user(self, user_id):
        try:
            return NewUser.objects.get(pk=user_id)
        except NewUser.DoesNotExist:
            return None



