from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from user_register.forms import RegistrationForm, UserChangeForm

# Create your views here.

def user_register(response):
    if response.method == 'POST':
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('user_home')
    else:
        form = RegistrationForm()

    return render(response, 'user_register/register.html', {'form': form})

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('user_home')