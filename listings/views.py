from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import Listing, Pending, Accepted
from .forms import UserForm, OfferForm, OfferResponseForm, PosterCounterOfferForm


# Create your views here.
def index(request):
	latest_posts = Listing.objects.order_by("-pub_date")
	template = loader.get_template("listings/index.html")
	context = {"latest_posts": latest_posts}
	return HttpResponse(template.render(context, request))

def user_listings(request):
	if request.user.profile.partner:
		user_posts = Listing.objects.filter(Q(user_id=request.user) | Q(user_id = request.user.profile.partner))
	else:	
		user_posts = Listing.objects.filter(user_id=request.user)
	offer = Pending.objects.filter(Q(u1=request.user.id) | Q(u2=request.user.id) | Q(u3=request.user.id) | Q(u4=request.user.id))
	accepted = Accepted.objects.filter(Q(u1=request.user.id) | Q(u2=request.user.id) | Q(u3=request.user.id) | Q(u4=request.user.id))
	template = loader.get_template("listings/mylistings.html")
	context = {"user_posts": user_posts,
			"pending": offer,
			"accepted": accepted}
	return HttpResponse(template.render(context, request))

def listing_details(request, pid):
	curr = request.user
	post = Listing.objects.get(id=pid)
	
	partner = None
	form = None

	if curr.is_authenticated:
		if hasattr(curr, 'profile') and hasattr(curr.profile, 'partner'):
			partner = curr.profile.partner

		if request.method == 'POST':
			form = OfferForm(request.POST, user=curr, partner=partner)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.u3 = curr.id
				obj.u1 = post.user.id
				obj.lid = post
				if partner:
					obj.u4 = partner.id
				if post.user.profile.partner:
					obj.u2 = post.user.profile.partner.id
				obj.save()
		else:
			form = OfferForm(user=curr, partner=partner)

	template = loader.get_template("listings/listingdetails.html")
	context = {
		"post": post,
		"form": form,
	}
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

def offer_details(request, pid, oid):
	curr = request.user
	post = Listing.objects.get(id=pid)
	otheritem = Listing.objects.get(id=oid)
	offer = Pending.objects.get(lid=pid, oid=oid)

	form = OfferResponseForm(request.POST or None)
	form2 = OfferForm(request.POST or None)
	form3 = PosterCounterOfferForm(request.POST or None)
	if request.method == 'POST':
		if 'submit_option' in request.POST:
			#offer accepted or rejected
			if request.POST.get('response') == 'option 1':
				Accepted.objects.create(
					lid=offer.lid,
					oid=offer.oid,
					lamount=offer.lamount,
					oamount=offer.oamount,
					partner_receiving=offer.partner_receiving,
					partner_sending=offer.partner_sending,
					u1=offer.u1,
					u2=offer.u2,
					u3=offer.u3,
					u4=offer.u4,
				)
				offer.delete()
			# Offer rejected
			elif request.POST.get('response') == 'option 2':
				offer.delete()
		if 'submit_counter' in request.POST:
			if form2.is_valid():
				return redirect('/users/profile')

	template = loader.get_template("listings/offerdetails.html")
	context = {"post": post,
			"offer": offer,
			"otheritem": otheritem,
			"curr": curr,
			"form": form,
			"form2": form2,
			"form3": form3}
	return HttpResponse(template.render(context, request))

def accepted_details(request, pid, oid):
    post = Listing.objects.get(id=pid)
    otheritem = Listing.objects.get(id=oid)
    trade = Accepted.objects.get(lid=pid, oid=oid)

    template = loader.get_template("listings/accepteddetails.html")
    context = {
        "post": post,
        "otheritem": otheritem,
        "trade": trade,
    }
    return HttpResponse(template.render(context, request))

def test(request, teststr):
	template = loader.get_template("listings/test.html")
	context = {"teststr":teststr}
	return HttpResponse(template.render(context,request))