from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

@login_required(login_url='login')
def index(request):
    user = request.user
    profile = user.profile
    friends = profile.friends.all()

    query = request.GET.get('q', '')  
    if query:
        friends = profile.friends.filter(username__icontains=query)
    else:
        friends = profile.friends.all()  

    return render(request, 'friends/index.html', {'friends': friends})