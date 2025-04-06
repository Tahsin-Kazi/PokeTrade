from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *

@login_required(login_url='login')
def index(request):
    user = request.user
    friends =

    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'name')

    if not user.is_authenticated:
        return redirect('login')

    if query:
        filter_kwargs = {f"{search_field}__icontains": query}
        friends =
    else:
        friends =

    context = {
        'user': user,
        'friendsList': friends,
        'search_query': query,
    }

    return render(request, 'friends/index.html', context)