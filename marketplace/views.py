from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time
from random import randint
from datetime import date
from .models import Listing
from .forms import OnMarketplacePokemon, EditPriceForm
from collection.models import Pokemon
from accounts.models import Profile

@login_required(login_url='login')
def index(request):
    listings = Listing.objects.all()
    return render(request, 'marketplace/index.html', {'marketplace':listings})


def add_to_listing():
    random_dex = randint(1, 1025)
    random_pokemon = fetch_pokemon(random_dex)
    if random_pokemon:
        Listing.objects.create(
            pokemon = random_pokemon,
            price = 200,
            date_posted = date.today(),
            status = "Not Sold",
            seller = "PokeTrade",
            buyer = None
        )
    else:
        print(f"There is no pokemon with that dex number")


def detail(request, pk):
    listing_id = get_object_or_404(Listing, id = pk)
    return render(request, 'marketplace/detail.html', {
        'listing' : listing_id
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = OnMarketplacePokemon(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user.profile
            listing.status = 'Not Sold'
            listing.save()
            deleted_pokemon = listing.pokemon
            request.user.profile.collection.remove(deleted_pokemon)
            request.user.profile.save()
            print(f"Removed {listing.pokemon} from {request.user.profile}'s collection")
            return redirect('detail', pk=listing.id)
        else:
            print(form.errors)
            messages.error(request, "There is an error creating the listing")
            return render(request, 'marketplace/form.html', {'form':form, 'title': 'New Listing'})
    form = OnMarketplacePokemon()
    return render(request, 'marketplace/form.html', {
        'form' : form,
        'title' : 'New Listing'
    })

@login_required
def edit(request,pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)

    form = EditPriceForm(request.POST or None, instance=listing)

    if request.method == 'POST' and listing.seller == request.user:
        if form.is_valid():
            form.save()
            messages.success(request, "Listing price updated successfully!")
            return redirect('detail', pk=listing.id)
        else:
            messages.error(request, "There was an error updating the price.")
    else:
        messages.error(request, "You are not not the pokemon's seller")
        return redirect('marketplace.index')

    return render(request, 'marketplace/form.html', {
        'form': form,
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

            request.user.profile.collection.add(pokemon)
            request.user.profile.save()

            listing.delete()

            messages.success(request, f"You have purchased {pokemon.name} from {listing.seller}!")
            return redirect('marketplace.index')
    else:
        # Error message if the user cannot afford the Pokémon or the listing is sold
        messages.error(request, "You do not have enough currency or the Pokémon has already been sold.")
        return redirect('marketplace.index')
    


