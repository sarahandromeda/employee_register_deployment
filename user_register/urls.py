from django.contrib.auth import views as auth_views 
from django.urls import path, include
from . import views
from user_register.views import PasswordChangeView

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('login/', views.login, name='login')
]