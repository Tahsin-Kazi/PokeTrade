from django.shortcuts import render
import keyboard, schedule, time
from random import randint


@loginIsNeeded
def buyPokemon(Pokemon, Listing, user, profile):
    if user.currency >= Listing.price:
        user.currency -= Listing.price
        Listing.remove(Pokemon)
        profile.collection.add(Pokemon, profile)

@loginIsNeeded
def editPrice(Pokemon, Listing, Profile):
    if Listing.Pokemon.seller == Profile.user:
        try:
            Listing.Pokemon.price == int(input('New Price: '))
        except ValueError:
            print('This is an invalid price. Please enter an integer')

def listingDeal(Listing):
    randomDex = randint(1, 1025)
    randomPokemon = fetch_pokemon(randomDex)
    Listing.add_pokemon(randomPokemon, Listing)

schedule.every(24).hours.do(listingDeal)



