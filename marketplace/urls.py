from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'marketplace.index'),
    path('collection/<int:listing_id>/', views.detail, name='detail'),
]