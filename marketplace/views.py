from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time
import schedule
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
            request.user.profile.collection.remove(listing.pokemon)
            print(f"Type of listing: {type(listing)}, Value of listing: {listing}")
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

def edit(request,pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)

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
    


