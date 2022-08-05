from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from user_register.models import NewUser

class RegistrationForm(forms.ModelForm):
    """
    Registration of New Users
    """
    password = forms.CharField(label='Password', widget = forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserCreationForm(forms.ModelForm):
    """
    User creation in terminal form
    """
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget = forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'first_name', 'last_name', 'is_staff', 'is_superuser']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords do not match.'))
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LoginEmailField(forms.Field):
    def validate(self, value):
        if NewUser.objects.get(email=value):
            super().validate(value)
        else:
            raise ValidationError

class UserAuthenticationForm(forms.ModelForm):
    """
    Login user form
    """
    email = LoginEmailField()

    class Meta:
        model = NewUser
        fields = ['password']
        widgets = {
            'password' : forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError(_('Invalid email or password. Note that both fields may be case sensitive.'))


class UserChangeForm(forms.ModelForm):
    """
    Password update form
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser']

    def clean_password(self):
        return self.initial['password'] 