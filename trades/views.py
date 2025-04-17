from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from collection.models import Pokemon
from accounts.models import Profile
from .models import *

@login_required(login_url='/login/')
def index(request):
    context = {
        "profile": request.user.profile,
        "friends": request.user.profile.friends.all(),
        "incoming_trades": Trade.objects.filter(receiver=request.user.profile, status="pending").all(),
        "outgoing_trades": Trade.objects.filter(sender=request.user.profile, status="pending").all()
    }
    return render(request, "trades/index.html", context=context)

@login_required(login_url='/login/')
def send(request, id):
    sender_profile = request.user.profile
    receiver_profile = get_object_or_404(Profile, id=id)

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
    return render(request, "trades/send.html", context)


@login_required
def view(request, id):
    trade = get_object_or_404(
        Trade.objects.select_related('sender', 'receiver')
        .prefetch_related('sender_pokemon', 'receiver_pokemon'),
        id=id
    )

    context = {
        'trade': trade,
        'sender_pokemon': trade.sender_pokemon.all(),
        'receiver_pokemon': trade.receiver_pokemon.all(),
    }

    if request.user.profile != trade.receiver:
        return render(request, "trades/view_sender.html", context)

    return render(request, 'trades/view.html', context)


@require_POST
@login_required
def process_trade(request, id):
    trade = get_object_or_404(Trade, id=id, receiver=request.user.profile)

    if 'accept_trade' in request.POST:
        if validate_trade(trade):
            transfer_pokemon(trade)
            trade.status = 'accepted'
            trade.save()
            messages.success(request, "Trade accepted! Pokemon have been traded.")
        else:
            trade.delete()
            messages.error(request, "Trade could not be completed. Some Pokemon are no longer available.")

    elif 'reject_trade' in request.POST:
        trade.delete()
        messages.info(request, "Trade rejected.")

    elif 'counter_trade' in request.POST:
        sender_id = trade.sender.id
        trade.delete()
        return redirect('trades.send', id=sender_id)

    return redirect('trades.index')


def validate_trade(trade):
    sender_owns_all = all(pokemon.owner == trade.sender for pokemon in trade.sender_pokemon.all())
    receiver_owns_all = all(pokemon.owner == trade.receiver for pokemon in trade.receiver_pokemon.all())
    return sender_owns_all and receiver_owns_all


def transfer_pokemon(trade):
    for pokemon in trade.sender_pokemon.all():
        pokemon.owner = trade.receiver
        pokemon.save()

    for pokemon in trade.receiver_pokemon.all():
        pokemon.owner = trade.sender
        pokemon.save()
        
        
@login_required
def cancel_trade(request, id):
    trade = get_object_or_404(Trade, id=id)

    trade.delete()
    messages.success(request, "Trade canceled successfully.")
    return redirect('trades.index')