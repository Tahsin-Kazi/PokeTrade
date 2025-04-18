from django.shortcuts import render
import keyboard, schedule, time
from random import randint
from datetime import date


@loginIsNeeded
def buyPokemon(Pokemon, Listing, user, profile):
    if user.currency >= Listing.price:
        user.currency -= Listing.price
        Listing.remove(Pokemon)
        profile.collection.add(Pokemon, profile)

@loginIsNeeded
def editPrice(pokemon, listing, profile):
    if listing.pokemon.seller == profile.user:
        try:
            edit_pokemon = listing.objects.get(pokemon = object_id)
            edit_pokemon.price = int

        except ValueError:
            print('This is an invalid price. Please enter an integer')

def add_to_listing(pokemon, Listing):
    randomDex = randint(1, 1025)
    randomPokemon = fetch_pokemon(randomDex)

    listing = Listing.objects.create (
        pokemon = randomPokemon,
        price = 200,
        date_posted = date.today(),
        status = "Not Sold",
        seller = "PokeTrade",
        buyer = None
    )
    listing.save()

schedule.every(24).hours.do(add_to_listing)



