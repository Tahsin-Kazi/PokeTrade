from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<int:id>/', views.detail, name='collection.detail'),
    path('', views.index, name='collection.index'),
]