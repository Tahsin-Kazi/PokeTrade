from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='marketplace.index'),
    path('new/', views.new, name='new'),
    path('listing/<int:pk>/', views.detail, name='detail'),
]