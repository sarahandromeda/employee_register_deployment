from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from user_register.forms import RegistrationForm, UserAuthenticationForm, UserChangeForm

# Create your views here.

def user_register(response):
    """
    User Registration View
    """
    if response.method == 'POST':
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success('Account created. Redirecting to login page...')
        return redirect('user_home')
    else:
        form = RegistrationForm()

    return render(response, 'user_register/register.html', {'form': form})

def login(response):
    """
    User Login View
    """
    user = response.user
    if user.is_authenticated:
        return redirect('user_home')
    if response.method == 'POST':
        form = UserAuthenticationForm(response.POST)
        email = response.POST.get('email')
        password = response.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(response, user)
            messages.success(response, 'Login Successful')
            return redirect('user_home')
    else:
        form = UserAuthenticationForm()

    return render(response, 'templates/login.html', {'form' : form})

class PasswordChangeView(PasswordChangeView):
    """
    User Change Password View
    """
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('user_home')