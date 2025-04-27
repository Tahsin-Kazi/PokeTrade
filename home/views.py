from django.shortcuts import render
from marketplace.models import Listing

def index(request):
    listing = Listing.objects.filter()


    return render(request, 'home/index.html')

def contact(request):
    return render(request, 'core/contact.html')