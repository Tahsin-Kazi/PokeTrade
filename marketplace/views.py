from django.shortcuts import render
import keyboard, random


@loginIsNeeded
def buyPokemon(Pokemon, Listing, user, profile):
    if user.currency >= Listing.price:
        user.currency -= Listing.price
        Listing.remove(Pokemon)
        user.Collection.add_pokemon(Pokemon, profile)

@loginIsNeeded
def editPrice(Pokemon, Listing, Profile):
    if Listing.Pokemon.seller == Profile.user:
        try:
            Listing.Pokemon.price == int(input('New Price: '))
        except ValueError:
            print('This is an invalid price. Please enter an integer')

def listingDeal(Listing):
    Listing.post_Pokemon(starters, )




