from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name = "home.index"),
    path("", views.index, name = "friends.index"),
    path('', views.index, name='collection.index'),
    # path("about/", views.about, name = "home.about")
]