from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

def user_login(request):
    template_data = {}
    template_data['title'] = 'Login'

    if request.method == 'POST':
        template_data['form'] = UserCreationForm()
        return render(request, 'accounts/login.html', {'template_data': template_data})