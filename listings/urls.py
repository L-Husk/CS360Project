from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mylistings", views.user_listings, name="user_listings"),
    path("<int:pid>/details", views.listing_details, name="listing_details"),
    path("form", views.listing_form, name="user_details)")
]