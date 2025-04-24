from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time
# import schedule
from random import randint
from datetime import date
from .models import Listing
from .forms import OnMarketplacePokemon
from collection.models import Pokemon
from accounts.models import Profile

@login_required(login_url='login')
def index(request):
    listings = Listing.objects.all()
    context = {
        'listing' : listings
    }
    return render(request, 'marketplace/index.html',context)



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

# def run_scheduler():
#     schedule.every(24).hours.do(add_to_listing)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


def detail(request, pk):
    listing_id = get_object_or_404(Listing, id = pk)
    return render(request, 'marketplace/detail.html', {'listing': listing_id})

@login_required
def new(request):
    if request.method == 'POST':
        form = OnMarketplacePokemon(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user.profile
            listing.save()
            request.user.profile.collection.remove(listing.pokemon)
            print(f"Type of listing: {type(listing)}, Value of listing: {listing}")
            return redirect('detail', pk=listing.id)
        else:
            print(form.errors)
            messages.error(request, "There is an error creating the listing")
            return render(request, 'marketplace.form.html', {'form':form, 'title': 'New Listing'})
    form = OnMarketplacePokemon()
    return render(request, 'marketplace/form.html', {
        'form' : form,
        'title' : 'New Listing'
    })

    


