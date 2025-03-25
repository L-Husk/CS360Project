from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mylistings", views.user_listings, name="user_listings")
]