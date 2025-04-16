from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import Listing
from .models import Pending
from .forms import UserForm
from .forms import OfferForm


# Create your views here.
def index(request):
	latest_posts = Listing.objects.order_by("-pub_date")
	template = loader.get_template("listings/index.html")
	context = {"latest_posts": latest_posts}
	return HttpResponse(template.render(context, request))

def user_listings(request):
	user_posts = Listing.objects.filter(user_id=request.user)
	template = loader.get_template("listings/mylistings.html")
	context = {"user_posts": user_posts}
	return HttpResponse(template.render(context, request))

def listing_details(request, pid):
	curr = request.user
	post = Listing.objects.filter(id=pid)
	form = OfferForm(request.POST)
	#offer = Pending.objects.filter(Q(u3=curr) | Q(u4=curr.profile.partner))
	if request.method == 'POST':
		if form.is_valid():
			obj = form.save(commit=False)
			
	template = loader.get_template("listings/listingdetails.html")
	context = {"post" : post,
			"form" : form}
	return HttpResponse(template.render(context, request))

def listing_form(request):
	form = UserForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			form = UserForm()
	return render(request, 'listings/form.html', {'form': form})