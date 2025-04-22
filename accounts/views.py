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
from django.db.models import Count
from accounts.models import Profile

# Altered Code
from django.views.decorators.http import require_POST
# Altered Code

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

@login_required
def friends_index(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'currency')  # Default sort: currency

    # Filter friends if a search is made
    friends = request.user.profile.get_friends()
    if query:
        friends = friends.filter(username__icontains=query)

    context = {
        'friends': friends,
        'sort_by': sort_by,
    }
    return render(request, 'friends/index.html', context)

@login_required
def leaderboard(request):
    sort_by = request.GET.get('sort', 'currency')  # Default sort: currency

    # Leaderboard: all users with their profile info and Pokémon count
    profiles = Profile.objects.annotate(pokemon_count=Count('collection'))

    if sort_by == 'pokemon':
        leaderboard = profiles.order_by('-pokemon_count', '-currency')
    else:
        leaderboard = profiles.order_by('-currency', '-pokemon_count')

    context = {
        'leaderboard': leaderboard,
        'sort_by': sort_by,
    }
    return render(request, 'friends/leaderboard.html', context)

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








# Altered Code

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)

    if friend_request.status == 'pending':
        friend_request.status = 'accepted'
        friend_request.save()

        # Add both users to each other's friend lists
        request.user.profile.friends.add(friend_request.from_user)
        friend_request.from_user.profile.friends.add(request.user)

        messages.success(request, f"You are now friends with {friend_request.from_user.username}!")
    else:
        messages.warning(request, "This friend request has already been handled.")

    return redirect('profile')

# Altered Code









@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        friend_request.status = 'rejected'
        friend_request.save()

    return redirect('incoming_requests')








# Altered Code

@login_required
@require_POST
def delete_friend_request(request, request_id):
    # Get the request the user sent
    fr = get_object_or_404(FriendRequest, id=request_id, from_user=request.user)

    if fr.status == 'pending':
        messages.error(request, "You can't delete a pending request. Cancel it instead.")
    elif fr.status == 'accepted':
        # Only delete the FriendRequest object — don't remove friendship
        fr.delete()
        messages.success(request, "Friend request removed. You are still friends.")
    elif fr.status == 'rejected':
        fr.delete()
        messages.success(request, "Rejected friend request removed.")

    return redirect('profile')

@login_required
@require_POST
def cancel_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, from_user=request.user)

    if fr.status == 'pending':
        fr.delete()
        messages.success(request, "Friend request canceled.")
    else:
        messages.error(request, "Only pending friend requests can be canceled.")

    return redirect('profile')

@login_required
def view_user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile = get_object_or_404(Profile, user=target_user)
    pokemon_collection = target_profile.collection.all()
    is_friend = target_user in request.user.profile.get_friends()

    return render(request, "accounts/friend_profile.html", {
        "target_user": target_user,
        "target_profile": target_profile,
        "pokemon_collection": pokemon_collection,
        "is_friend": is_friend,
    })

# Altered Code
