from django import forms
from .models import Listing
from accounts.models import Profile

INPUT_CLASS = 'w-full py-6 px-6 rounded-xl border'

class OnMarketplacePokemon(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pokemon', 'price', 'status','seller', 'buyer']

    widgets = {
        'pokemon' : forms.Select(attrs={
            'class' : INPUT_CLASS
        }),
        'price' : forms.TextInput(attrs={
            'class' : INPUT_CLASS
        }),
        'status' : forms.CharField(attrs={
            'class' : INPUT_CLASS
        }),
        'seller' : forms.HiddenInput(),
        'buyer' : forms.ModelChoiceField(
            queryset=Profile.objects.all(),
            required=False,
            widget=forms.Select(attrs={'class': 'w-full py-6 px-6 rounded-xl border'}),
            empty_label="Select Buyer"
        )

    }