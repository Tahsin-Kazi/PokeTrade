from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('trades/', views.index, name='trades.index'),
    path('trades/send/<int:pk>/', views.send_trade, name='trades.send_trade'),
]