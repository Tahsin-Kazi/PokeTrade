from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from random import randint
from datetime import date
from .models import Listing
from .forms import OnMarketplacePokemon, EditPriceForm
from collection.models import Pokemon

# INDEX PAGE: Show all marketplace listings
@login_required(login_url='login')
def index(request):
    listings = Listing.objects.all()
    return render(request, 'marketplace/index.html', {'marketplace': listings})

# RANDOM ADD (not used much - used for testing/demo maybe)
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
    else:
        print("There is no Pokémon with that dex number.")

# VIEW DETAILS OF A SINGLE LISTING
def detail(request, pk):
    listing = get_object_or_404(Listing, id=pk)
    return render(request, 'marketplace/detail.html', {'listing': listing})

# CREATE A NEW LISTING
@login_required
def new(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = OnMarketplacePokemon(request.POST, user=profile)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = profile
            listing.status = 'Not Sold'
            listing.save()

            # Remove the Pokémon from user's collection after listing
            profile.collection.remove(listing.pokemon)
            profile.save()

            messages.success(request, f"{listing.pokemon.name} has been listed for sale!")
            return redirect('detail', pk=listing.id)
        else:
            messages.error(request, "There was an error creating the listing.")
    else:
        form = OnMarketplacePokemon(user=profile)

    return render(request, 'marketplace/form.html', {
        'form': form,
        'title': 'New Listing'
    })

# EDIT THE PRICE OF A LISTING
@login_required
def edit(request, pk):
    profile = request.user.profile
    listing = get_object_or_404(Listing, pk=pk, seller=profile)

    form = EditPriceForm(request.POST or None, instance=listing)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Listing price updated successfully!")
            return redirect('detail', pk=listing.id)
        else:
            messages.error(request, "There was an error updating the price.")

    return render(request, 'marketplace/form.html', {
        'form': form,
        'title': 'Edit Price'
    })

# BUY A POKEMON
@login_required
def buyPokemon(request, pk):
    listing = get_object_or_404(Listing, id=pk)
    profile = request.user.profile

    if profile.currency >= listing.price and listing.status == "Not Sold":
        with transaction.atomic():
            profile.currency -= listing.price
            profile.collection.add(listing.pokemon)
            profile.save()

            listing.delete()

            messages.success(request, f"You have purchased {listing.pokemon.name}!")
            return redirect('marketplace.index')
    else:
        messages.error(request, "You do not have enough currency or the Pokémon has already been sold.")
        return redirect('marketplace.index')
