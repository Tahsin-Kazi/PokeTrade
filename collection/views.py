from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
import requests

@login_required(login_url='login')
def index(request):
    return render(request, 'collection/index.html', {'user' : request.user, 'collection' : request.user.profile.collection.all()})

def detail(request, pk):
    p = get_object_or_404(Pokemon, pk=pk)
    return render(request,'collection/details.html', {'data': p.data})


def create_pokemon(name):
    p = Pokemon.objects.create()
    p.name = name
    p.pokemon = name
    # PLACEHOLDER IMAGE - WILL BE REPLACED
    p.image = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Pokebola-pokeball-png-0.png/481px-Pokebola-pokeball-png-0.png"
    p.data = requests.get("https://pokeapi.co/api/v2/pokemon/" + name).json()
    p.save()
    return p