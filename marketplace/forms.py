from django import forms
from .models import Listing

class OnMarketplacePokemon(forms.ModelForm):
    class Meta:
        fields = ('pokemon', 'price', 'date_posted', 'status', 'buyer', 'seller')