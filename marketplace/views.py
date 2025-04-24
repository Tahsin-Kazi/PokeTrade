from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import time
import schedule
from random import randint
from datetime import date
from .models import Listing
from .forms import OnMarketplacePokemon
from accounts.models import Profile

@login_required(login_url='login')
def index(request):
    listings = Listing.objects.all()
    context = {
        'listing' : listings
    }
    return render(request, 'marketplace/index.html',context)

@login_required
def buyPokemon(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    pokemon = listing.pokemon
    user = request.user
    profile = user.profile
    if user.currency >= listing.price and listing.status == "Not Sold":
        with transaction.atomic():
            user.currency -= listing.price
            user.save()
            listing.status = "Sold"
            listing.buyer = user
            profile.collection.add(pokemon)
            messages.success(request, f"You have purchased {pokemon.name} from {listing.seller}!")
            return redirect('marketplace.index')
    else:
        messages.error(request, "You do not have enough")
        return redirect('marketplace.index')

@login_required
def editPrice(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if listing.seller == request.user:
        if request.method == 'POST':
            try:
                new_price = int(request.POST.get('price'))
                if new_price >= 0:
                    listing.price = new_price
                    listing.save()
                    messages.sussess(request, "Price updated")
                    return redirect('marketplace.index')
                else:
                    messages.error(request, "This price is negative")
            except ValueError:
                messages.error(request, "Invalid proce. Please enter an non-negative integer")
        return render(request, 'edit_price.html', {'listing': listing})
    else:
        messages.error(request, "You did not put this pokemon on the marketplace so you" \
        "cannot edit its price")
        return redirect('marketplace.index')

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

def run_scheduler():
    schedule.every(24).hours.do(add_to_listing)
    while True:
        schedule.run_pending()
        time.sleep(1)

def all_pokemon(request):
    listings = Listing.pokemon.all()
    return render(request, 'index.html', {'listings': listings})

def detail(request, listing_id):
    listing_id = get_object_or_404(Listing, id = listing_id)


    return render(request, 'item/detail.html', {
        'listing' : listing_id
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = OnMarketplacePokemon(request.POST)
        Listing = form.save(commit=False)
        Listing.save()
        Profile.collection.remove(Listing.pokemon)
        
        return redirect('listing:detail', pk=listing.pokemon)
                
    
    form = OnMarketplacePokemon()
    return render(request, 'marketplace/form.html', {
        'form' : form,
        'title' : 'New Listing'
    })

    


