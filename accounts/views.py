from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def register(request):
    template_data = {'title': 'Register'}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")  # Redirect to landing page
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "template_data": template_data})

def user_login(request):
    template_data = {'title': 'Login'}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect(profile)  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form, "template_data": template_data})

def user_logout(request):
    logout(request)  # Logs the user out
    return redirect(index)  # Redirect to the landing page (or any other page)

@login_required
def profile(request):
    user = request.user
    template_data = {
        'title': 'Profile',
        # 'reviews': Review.objects.filter(user=user).order_by('-created_at'),
        # 'orders': get_orders(user),
    }
    return render(request, "accounts/profile.html", {"user": user, "template_data": template_data})

# @login_required
# def library(request):
#     user = request.user
#     template_data = {
#         'title': 'Library',
#         'library': get_library(user),
#     }
#     return render(request, "accounts/library.html", {"user": user, "template_data": template_data})
#
# def get_orders(user):
#     p = Profile.objects.get(user=user)
#     return Order.objects.filter(profile=p).order_by('-created_at')
#
# def get_library(user):
#     temp = Profile.objects.get(user=user).purchasedMovies
#     res = []
#     for movie_id, quantity in temp.items():
#         res.append((get_object_or_404(Movie, id=movie_id), quantity))
#     return res