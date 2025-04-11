from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from collection.models import Pokemon
from accounts.models import Profile
from .models import *

@login_required(login_url='/login/')
def index(request):
    return render(request, "trades/index.html", context={"profile": request.user.profile, "friends" : request.user.profile.friends.all()})

@login_required(login_url='/login/')
def send_trade(request, pk):
    sender_profile = request.user.profile
    receiver_profile = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        # Handle trade creation
        if 'create_trade' in request.POST:
            trade = Trade.objects.create(
                sender=sender_profile,
                receiver=receiver_profile,
                status='pending'
            )

            # Add selected Pokemon to the trade
            sender_pokemon_ids = request.POST.getlist('sender_pokemon')
            receiver_pokemon_ids = request.POST.getlist('receiver_pokemon')

            for pokemon_id in sender_pokemon_ids:
                pokemon = get_object_or_404(Pokemon, id=pokemon_id, owner=sender_profile)
                trade.sender_pokemon.add(pokemon)

            for pokemon_id in receiver_pokemon_ids:
                pokemon = get_object_or_404(Pokemon, id=pokemon_id, owner=receiver_profile)
                trade.receiver_pokemon.add(pokemon)

            messages.success(request, "Trade offer sent successfully!")
            return redirect('trades.index')

        # Handle trade cancellation
        elif 'cancel_trade' in request.POST:
            return redirect('trades.index')

    # Get available Pokemon for both parties
    sender_pokemon = Pokemon.objects.filter(owner=sender_profile)
    receiver_pokemon = Pokemon.objects.filter(owner=receiver_profile)

    context = {
        'sender': sender_profile,
        'receiver': receiver_profile,
        'sender_pokemon': sender_pokemon,
        'receiver_pokemon': receiver_pokemon,
    }
    return render(request, "trades/send_trade.html", context)