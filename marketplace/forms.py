from django import forms
from .models import Listing
from accounts.models import Profile

INPUT_CLASS = 'w-full py-6 px-6 rounded-xl border'

class OnMarketplacePokemon(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['pokemon', 'price', 'status']
        widgets = {
            'pokemon': forms.Select(attrs={'class': INPUT_CLASS}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'status': forms.Select(attrs={'class': INPUT_CLASS}),  # Use Select for status since it's a choice field
        }

    buyer = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': INPUT_CLASS}),
        empty_label="Select Buyer"
    )
