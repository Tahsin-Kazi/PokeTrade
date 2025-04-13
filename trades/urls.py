from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('trades/', views.index, name='trades.index'),
    path('trades/send/<int:id>/', views.send, name='trades.send'),
    path('trades/view/<int:id>/', views.view, name='trades.view'),
    path('trade//process/<int:id>', views.process_trade, name='trade.process'),
]