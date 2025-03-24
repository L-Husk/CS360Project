from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Listing


# Create your views here.
def index(request):
    latest_posts = Listing.objects.order_by("-pub_date")
    template = loader.get_template("listings/index.html")
    context = {"latest_posts": latest_posts}
    return HttpResponse(template.render(context, request))