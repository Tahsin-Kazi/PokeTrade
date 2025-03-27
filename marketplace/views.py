from django.shortcuts import render

def postPokemon(request, id):
    Pokemon = get_object__or_404(request, dexNumber)
    template_data = {
        'name' = Pokemon.name,
        price = input('Price: ')
    }

    if request.method == 'POST':
        return


def editPrice(request):

return redirect('marketplace.show')



