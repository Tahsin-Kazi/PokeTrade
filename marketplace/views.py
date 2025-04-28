from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from random import randint
from datetime import date
from .models import Listing
from collection.models import Pokemon
from accounts.models import Profile
from pokebase import pokemon as fetch_pokemon

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
    listings = Listing.objects.all()
    return render(request, 'marketplace/index.html', {'marketplace':listings})



def add_to_marketplace(profile):
    x, y, z = randint(1, 1025), randint(1, 1025), randint(1, 1025)
    x, y, z = fetch_pokemon(x), fetch_pokemon(y), fetch_pokemon(z)

    if x:
        Listing.objects.create(
            pokemon=x,
            price=200,
            date_posted=date.today(),
            status="Not Sold",
            seller="PokeTrade", 
            buyer=None
        )
        print(f"Added {x.name} to the marketplace")
    if y:
        Listing.objects.create(
            pokemon=y,
            price=200,
            date_posted=date.today(),
            status="Not Sold",
            seller="PokeTrade", 
            buyer=None
        )
        print(f"Added {y.name} to the marketplace")
    if z:
        Listing.objects.create(
            pokemon=z,
            price=200,
            date_posted=date.today(),
            status="Not Sold",
            seller="PokeTrade", 
            buyer=None
        )
        print(f"Added {z.name} to the marketplace")


@login_required
def detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    data = listing.pokemon.data
    data['types_with_colors'] = [
        {"type": t, "color": TYPE_COLORS.get(t, "bg-gray-200")} for t in data.get("types", [])
    ]

    if request.method == 'POST' and 'edit_price' in request.POST:
        if listing.seller.user == request.user:
            new_price = request.POST.get('price', None)
            if new_price:
                try:
                    listing.price = float(new_price)
                    listing.save()
                    messages.success(request, "Price updated successfully!")
                except ValueError:
                    messages.error(request, "Invalid price value.")
            else:
                messages.error(request, "Price is required.")
            return redirect('detail', pk=listing.pk)  
    return render(request, 'marketplace/detail.html', {
        'listing': listing, 'data': data
    })


@login_required
def new(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon')
        price = request.POST.get('price')
        try:
            pokemon = profile.collection.get(id=pokemon_id)
        except Pokemon.DoesNotExist:
            pokemon = None

        if not pokemon:
            messages.error(request, "You can only list Pokémon that belong to you.")
        elif not price.isdigit() or int(price) <= 0:
            messages.error(request, "The price must be a positive number.")
        else:
            Listing.objects.create(
                pokemon=pokemon,
                price=int(price),
                seller=profile,
                status="Not Sold"
            )
            request.user.profile.collection.remove(pokemon)
            messages.success(request, f'{pokemon.name} listed successfully!')
            return redirect('marketplace.index')

    pokemon_choices = profile.collection.all()
    return render(request, 'marketplace/form.html', {
        'title': 'New Listing',
        'pokemon_choices': pokemon_choices
    })




@login_required
def edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)

    if request.method == 'POST':
        price = request.POST.get('price')

        if price and price.isdigit():
            listing.price = float(price)
            listing.save()

            messages.success(request, "Listing price updated successfully!")
            return redirect('detail', pk=listing.id)
        else:
            messages.error(request, "Invalid price entered. Please enter a valid price.")

    return render(request, 'marketplace/form.html', {
        'listing': listing,
        'title': 'Edit Price'
    })

@login_required
def deleteListing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        with transaction.atomic():
            pokemon = listing.pokemon
            profile.collection.add(pokemon)
            pokemon.owner = profile
            pokemon.save()
            listing.delete()
            messages.success(request, f"You have removed {pokemon.name} from the marketplace!")
            return redirect('marketplace.index')
    else:
        return redirect('detail', pk=pk)


@login_required
def buyPokemon(request, pk):
    listing = get_object_or_404(Listing, id=pk)
    user = request.user
    profile = user.profile
    
    if profile.currency >= listing.price:
        with transaction.atomic():
            pokemon = listing.pokemon

            profile.currency -= listing.price
            profile.save()
            listing.seller.currency += listing.price
            listing.seller.save()

            profile.collection.add(pokemon)
            pokemon.owner = profile
            pokemon.save()

            listing.delete()

            messages.success(request, f"You have purchased {pokemon.name} from {listing.seller}!")
            return redirect('marketplace.index')
    else:
        # Error message if the user cannot afford the Pokémon or the listing is sold
        messages.error(request, "You do not have enough currency or the Pokémon has already been sold.")
        return redirect('marketplace.index')
    





