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
    sent_requests = FriendRequest.objects.filter(from_user=user)
    received_requests = FriendRequest.objects.filter(to_user=user)

    template_data = {
        'title': 'Profile',
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }

    return render(request, "accounts/profile.html", {
        "user": user,
        "template_data": template_data,
        "sent_requests": sent_requests,
        "received_requests": received_requests,
    })

def friends_index(request):
    user = request.user
    profile = user.profile
    friends = profile.friends.all()

    query = request.GET.get('q', '')
    if query:
        friends = profile.friends.filter(username__icontains=query)
    else:
        friends = profile.friends.all()

    return render(request, 'friends/index.html', {'friends': friends})


@login_required
def find_friends(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)  # Exclude self

    if query:
        users = users.filter(username__icontains=query)

    # Check which users have already been sent requests or are friends
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    sent_user_ids = [req.to_user.id for req in sent_requests]
    friends_ids = [friend.id for friend in request.user.profile.get_friends()]

    return render(request, "accounts/find_friends.html", {
        "users": users,
        "sent_user_ids": sent_user_ids,
        "friends_ids": friends_ids,
        "query": query,
    })


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if to_user != request.user:
        FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

    return redirect('find_friends')

@login_required
def incoming_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'accounts/incoming_requests.html', {'requests': requests})


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        friend_request.status = 'accepted'
        friend_request.save()

        # Add both as friends
        friend_request.from_user.profile.friends.add(friend_request.to_user)
        friend_request.to_user.profile.friends.add(friend_request.from_user)

    return redirect('incoming_requests')

@login_required
@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        friend_request.status = 'rejected'
        friend_request.save()

    return redirect('incoming_requests')

@login_required
def view_user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    is_friend = target_user in request.user.profile.get_friends()

    return render(request, "accounts/user_profile.html", {
        "target_user": target_user,
        "is_friend": is_friend,
    })
