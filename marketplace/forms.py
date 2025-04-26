from django import forms
from .models import Listing
from accounts.models import Profile

INPUT_CLASS = 'w-full py-6 px-6 rounded-xl border'

class OnMarketplacePokemon(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pokemon', 'price']
        widgets = {
            'pokemon': forms.Select(attrs={'class': INPUT_CLASS}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class EditPriceForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['price']
        widgets = {
            'price': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }
        