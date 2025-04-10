from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.text import capfirst
from .models import *
from random import randint

TYPE_COLORS = {
    "Normal": "bg-gray-400",
    "Fire": "bg-red-500",
    "Water": "bg-blue-500",
    "Electric": "bg-yellow-400",
    "Grass": "bg-green-500",
    "Ice": "bg-blue-300",
    "Fighting": "bg-red-700",
    "Poison": "bg-purple-500",
    "Ground": "bg-yellow-600",
    "Flying": "bg-blue-400",
    "Psychic": "bg-pink-500",
    "Bug": "bg-green-600",
    "Rock": "bg-yellow-700",
    "Ghost": "bg-purple-700",
    "Dragon": "bg-indigo-500",
    "Dark": "bg-gray-700",
    "Steel": "bg-gray-500",
    "Fairy": "bg-pink-300",
}

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

def detail(request, id):
    
    p = get_object_or_404(Pokemon, id=id)

    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        if new_name:
            p.name = new_name
            p.save()
            messages.success(request, "Nickname updated successfully!")
        else:
            messages.error(request, "Nickname is invalid!")

    data = p.data
    data['image'] = p.image
    data['nickname'] = p.name
    data['total'] = sum(data['stats'].values())
    data['id'] = p.id
    
    data['types_with_colors'] = [
        {"type": t, "color": TYPE_COLORS.get(t, "bg-gray-200")} for t in data.get("types", [])
    ]

    return render(request,'collection/details.html', {'data': data})

def add_pokemon(name, pokemon, profile):
    p = Pokemon(
        name = name,
        pokemon = pokemon,
        owner = profile,
    )
    p.save()
    profile.collection.add(p)
    return p

def add_starters(profile):
    x, y, z = randint(1, 1000), randint(1, 1000), randint(1, 1000)
    x, y, z = fetch_pokemon(x), fetch_pokemon(y), fetch_pokemon(z)
    add_pokemon(capfirst(x.name), x.name, profile)
    add_pokemon(capfirst(y.name), y.name, profile)
    add_pokemon(capfirst(z.name), z.name, profile)

def database_filler(i):
    profile = User.objects.all()[i].profile
    names = {1 : "Ahad", 2 : "Kazi", 3 : "Matthew", 4 : "Jason"}
    pokemons = {1 : "pikachu", 2 : "ditto", 3 : "clefairy", 4 : "bulbasaur", 5 : "charizard"}
    for x in range(3):
        add_pokemon(names[randint(1, 4)], pokemons[randint(1, 5)], profile)