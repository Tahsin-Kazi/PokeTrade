from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<int:pk>/', views.detail, name='poketrade.detail'),
    path('collection/', views.index, name='poketrade.index'),
]