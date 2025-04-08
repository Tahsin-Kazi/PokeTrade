from django.urls import models
from . import views

urlpatterns = [
    path('', views.marketplace, name = 'marketplace.index'),
]