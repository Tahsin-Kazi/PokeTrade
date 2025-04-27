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



@login_required(login_url='login')
def index(request):
    listings = Listing.objects.all()
    return render(request, 'marketplace/index.html', {'marketplace':listings})


def add_to_listing():
    random_dex = randint(1, 1025)  
    random_pokemon = fetch_pokemon(random_dex)  
    if random_pokemon:
        Listing.objects.create(
            pokemon=random_pokemon,  
            price=200,  
            date_posted=date.today(),  
            status="Not Sold",  
            seller="PokeTrade",  
            buyer=None  
        )
        print(f"Added {random_pokemon.name} to the marketplace")
    else:
        print("There is no Pokémon with that Dex number")

def add_starters(profile):
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
        'listing': listing
    })


def new(request):
    user = request.user
    profile = user.profile

    # Get all Pokémon in the user's collection
    pokemon_choices = profile.collection.all()

    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon')
        price = request.POST.get('price')

        # Ensure the Pokémon exists in the collection and the price is valid
        pokemon = profile.collection.filter(id=pokemon_id).first()

        if pokemon and price.isdigit():
            # Create the listing
            Listing.objects.create(
                pokemon=pokemon,
                price=price,
                seller=profile,
                status="Not Sold"
            )
            # Add success message and redirect
            messages.success(request, f'{pokemon.name} listed successfully!')
            return redirect('marketplace.index')
        else:
            messages.error(request, "There was an issue with your listing.")

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
def buyPokemon(request, pk):
    listing = get_object_or_404(Listing, id=pk)
    user = request.user
    profile = user.profile
    
    if profile.currency >= listing.price and listing.status == "Not Sold":
        with transaction.atomic():
            pokemon = listing.pokemon

            profile.currency -= listing.price
            profile.save()

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
    

