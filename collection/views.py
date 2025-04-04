from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *
import requests

from random import randint

@login_required(login_url='login')
def index(request):
    collection = request.user.profile.collection.all()
    search_query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'name')

    if search_query:
        filter_kwargs = {
            f"{search_field}__icontains": search_query
        }
        collection = collection.filter(**filter_kwargs)

    context = {
        'user': request.user,
        'collection' : collection,
        'search_query': search_query,
    }

    return render(request, 'collection/index.html', context)

def detail(request, pk):
    p = get_object_or_404(Pokemon, pk=pk)
    return render(request,'collection/details.html', {'data': p.data})

def create_pokemon(profile, name, pokemon, image):
    p = Pokemon.objects.create()
    p.name = name
    p.pokemon = pokemon
    p.owner = profile
    p.image = image
    p.data = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon).json()
    p.save()
    profile.collection.add(p)
    profile.save()
    return p

def database_filler():
    profile = User.objects.first().profile
    pokemons = {1 : "pikachu", 2 : "ditto", 3 : "clefairy", 4 : "bulbasaur", 5 : "charizard"}
    for x in range(10):
        create_pokemon(profile, "pet" + str(x), str(pokemons[randint(1, 5)]), "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pokebola-pokeball-png-0.png/481px-Pokebola-pokeball-png-0.png")