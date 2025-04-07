from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

@login_required(login_url='login')
def index(request):
    user = request.user
    friends = user.profile.friends.all()

    return render(request, 'friends/index.html', {'friends': friends})