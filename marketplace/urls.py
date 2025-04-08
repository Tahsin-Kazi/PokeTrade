from django.urls import models
from . import views

urlpatterns = [
    path('marketplace/', views.marketplace, name = 'marketplace'),
]