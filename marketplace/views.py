from django.shortcuts import render
import keyboard

@loginIsNeeded
def postPokemon(request, Pokemon):
    Pokemon = get_object__or_404(request, dexNumber)
    template_data = {
        'name' = Pokemon.name,
        price = input('Price: ')
    }

    if request.method == 'POST':
        return

@loginIsNeeded
def buyPokemon(marketPlacePokemon):


@loginIsNeeded
def editPrice(marketPlacePokemon):
    if marketPlacePokemon.seller == account.username:
        try:
            marketPlacePokemon.price == int(input('New Price: '))
        except ValueError:
            print('This is an invalid price. Please enter an integer')




