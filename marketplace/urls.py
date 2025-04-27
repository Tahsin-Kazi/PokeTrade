from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='marketplace.index'),
    path('new/', views.new, name='marketplace_new'),
    path('listing/<int:pk>/', views.detail, name='detail'),
    path('marketplace/listing/<int:pk>/buy/', views.buyPokemon, name='buy'),
    path('listing/<int:pk>/edit/', views.edit, name='marketplace_edit_price'),
]