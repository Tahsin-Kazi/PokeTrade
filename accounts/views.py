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
from home.views import index as home_view
from collection.views import index as collection_view
from django.contrib import messages
from .models import FriendRequest, send_friend_request, accept_friend_request, reject_friend_request

def register(request):
    template_data = {'title': 'Register'}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "You have successfully registered! Go to Collection to see your starters!")
            return redirect(user_login)  # Redirect to landing page
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
                login(request, user)  
                messages.success(request, "You have successfully logged in!")  # Success message
                return redirect(home_view)  # Redirect to the home page
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form, "template_data": template_data})

def user_logout(request):
    logout(request)  # Logs the user out
    messages.success(request, "You have successfully logged out!")
    return redirect(home_view)  # Redirect to the landing page (or any other page)

@login_required
def profile(request):
    user = request.user
    template_data = {
        'title': 'Profile',
        # 'reviews': Review.objects.filter(user=user).order_by('-created_at'),
        # 'orders': get_orders(user),
    }

    from django.shortcuts import render, redirect

    return render(request, "accounts/profile.html", {"user": user, "template_data": template_data})

@login_required
def friends_index(request):
    return render(request, 'accounts/friends_index.html')  # or your appropriate template

@login_required
def send_request_view(request, user_id):
    from_user = request.user
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    return redirect('home')

@login_required
def accept_request_view(request, request_id):
    accept_friend_request(request_id)
    return redirect('friend_requests')

@login_required
def reject_request_view(request, request_id):
    reject_friend_request(request_id)
    return redirect('friend_requests')

@login_required
def friend_requests_view(request):
    incoming_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'friends/requests.html', {'requests': incoming_requests})
