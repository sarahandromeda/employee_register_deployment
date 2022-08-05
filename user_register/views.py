from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
            return render(response, 'user_register/register.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(response, 'user_register/register.html', {'form': form})

def login_view(response):
    """
    User Login View
    """
    if response.method == 'POST':
        form = UserAuthenticationForm(response.POST)
        if form.is_valid():
            email = response.POST.get('email')
            password = response.POST.get('password')
            user = authenticate(response, email=email, password=password)
            if user is not None:
                login(response, user)
                messages.success(response, 'Login Successful')
                return redirect('user_home')
        else:
            return render(response, 'registration/login.html', {'form' : form})
    else:
        form = UserAuthenticationForm()

    return render(response, 'registration/login.html', {'form' : form})

class PasswordChangeView(PasswordChangeView):
    """
    User Change Password View
    """
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('user_home')