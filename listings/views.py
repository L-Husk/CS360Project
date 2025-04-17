from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import Listing, Pending
from .forms import UserForm, OfferForm, OfferResponseForm, PosterCounterOfferForm


# Create your views here.
def index(request):
	latest_posts = Listing.objects.order_by("-pub_date")
	template = loader.get_template("listings/index.html")
	context = {"latest_posts": latest_posts}
	return HttpResponse(template.render(context, request))

def user_listings(request):
	user_posts = Listing.objects.filter(user_id=request.user)
	offer = Pending.objects.filter(Q(u1=request.user.id) | Q(u2=request.user.id) | Q(u3=request.user.id) | Q(u4=request.user.id)).values_list('lid', flat=True)
	user_pending = Listing.objects.filter(id__in=offer)
	template = loader.get_template("listings/mylistings.html")
	context = {"user_posts": user_posts,
			"pending": user_pending}
	return HttpResponse(template.render(context, request))

def listing_details(request, pid):
	curr = request.user
	post = Listing.objects.get(id=pid)
	form = OfferForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			obj = form.save(commit=False)
			obj.u3 = request.user.id
			obj.u1 = post.user.id
			obj.lid = post
			obj.save()
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

def offer_details(request, pid):
	curr = request.user
	post = Listing.objects.get(id=pid)
	offer = Pending.objects.get(lid=pid)
	otheritem = Listing.objects.get(id=offer.oid.id)
<<<<<<< Updated upstream
	form = OfferResponseForm(request.POST or None)
	form2 = OfferForm(request.POST or None)
	form3 = PosterCounterOfferForm(request.POST or None)
	if request.method == 'POST':
		if 'submit_response' in request.POST:
			if form.is_valid(): #offer accepted or rejected
				''
		if 'submit_counter' in request.POST:
			if form2.is_valid(): #counter offer
				return redirect('/users/profile')
		if 'submit_postcounter' in request.POST:
			if form3.is_valid():
				''
=======
>>>>>>> Stashed changes
	template = loader.get_template("listings/offerdetails.html")
	context = {"post": post,
			"offer": offer,
			"otheritem": otheritem,
<<<<<<< Updated upstream
			"curr": curr,
			"form": form,
			"form2": form2,
			"form3": form3}
=======
>>>>>>> Stashed changes
	return HttpResponse(template.render(context, request))