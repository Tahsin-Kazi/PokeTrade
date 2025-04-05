from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import requests

from random import randint

@login_required(login_url='login')
def index(request):
    user = request.user
    collection = user.profile.collection.all()
    
    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'name')
    
    if not user.is_authenticated:
        return redirect('login')

    if query:
        filter_kwargs = {f"{search_field}__icontains": query}
        collection = Pokemon.objects.filter(owner=user.profile, **filter_kwargs)
    else:
        collection = Pokemon.objects.filter(owner=user.profile)

    context = {
        'user': user,
        'collection' : collection,
        'search_query': query,
    }

    return render(request, 'collection/index.html', context)

def detail(request, pk):
    p = get_object_or_404(Pokemon, pk=pk)
    return render(request,'collection/details.html', {'data': p.data})

def create_pokemon(name, pokemon, profile):
    p = Pokemon(
        name = name,
        pokemon = pokemon,
        owner = profile,
    )
    p.save()
    return p

def database_filler():
    profile = User.objects.first().profile
    pokemons = {1 : "pikachu", 2 : "ditto", 3 : "clefairy", 4 : "bulbasaur", 5 : "charizard"}
    for x in range(10):
        create_pokemon(profile, "pet" + str(x), str(pokemons[randint(1, 5)]), "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pokebola-pokeball-png-0.png/481px-Pokebola-pokeball-png-0.png")