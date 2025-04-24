from django import forms
from .models import Listing
from accounts.models import Profile

INPUT_CLASS = 'w-full py-6 px-6 rounded-xl border'

class OnMarketplacePokemon(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('pokemon', 'price', 'status','seller', 'buyer')

    widgets = {
        'pokemon' : forms.Select(attrs={
            'class' : INPUT_CLASS
        }),
        'price' : forms.TextInput(attrs={
            'class' : INPUT_CLASS
        }),
        'status' : forms.TextInput(attrs={
            'class' : INPUT_CLASS
        }),
        'seller' : forms.TextInput(attrs={
            'class' : Profile.user
        }),
        'buyer' : forms.TextInput(attrs={
            'class' : "None"
        })

    }