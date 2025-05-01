from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from .models import Listing, Pending, Accepted
from .forms import UserForm, OfferForm, OfferResponseForm, HashVerificationForm
from decimal import Decimal
import hashlib
import secrets


# Create your views here.
def index(request):
	latest_posts = Listing.objects.exclude(amount=0).order_by("-pub_date")
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
				if not Pending.objects.filter(lid=post, oid=obj.oid):
					obj.u3 = curr.id
					obj.u1 = post.user.id
					obj.lid = post
					if partner:
						obj.u4 = partner.id
					if post.user.profile.partner:
						obj.u2 = post.user.profile.partner.id
					obj.save()
					return redirect("/listings/mylistings")
		else:
			form = OfferForm(user=curr, partner=partner)
	collected = 3
	if post.is_alive:
		collected += 5
	if post.is_chilled:
		collected += 3
	if post.is_fragile:
		collected += 2
	template = loader.get_template("listings/listingdetails.html")
	context = {
		"post": post,
		"form": form,
		"collected": collected
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
			return redirect("/listings/mylistings")
	return render(request, 'listings/form.html', {'form': form})

def offer_details(request, pid, oid):
	curr = request.user
	post = Listing.objects.get(id=pid)
	otheritem = Listing.objects.get(id=oid)
	offer = Pending.objects.get(lid=pid, oid=oid)
	postcollected = 3
	offercollected = 3
	postcollected = postcollected+5 if post.is_alive else postcollected
	postcollected = postcollected+3 if post.is_chilled else postcollected
	postcollected = postcollected+2 if post.is_fragile else postcollected
	offercollected = offercollected+5 if otheritem.is_alive else offercollected
	offercollected = offercollected+3 if otheritem.is_chilled else offercollected
	offercollected = offercollected+2 if otheritem.is_fragile else offercollected

	form = OfferResponseForm(request.POST or None)
	form2 = OfferForm(request.POST or None)
	if request.method == 'POST':
		if 'submit_option' in request.POST:
			#offer accepted or rejected
			if request.POST.get('response') == 'option 1':
				if request.user.id == offer.u1 or request.user.id == offer.u2:
					offer.postpartner_receiving=request.POST.get('partner_receiving')
				if request.user.id == offer.u3 or request.user.id == offer.u4:
					offer.offerpartner_receiving=request.POST.get('partner_receiving')
				hashinput = secrets.token_hex(16)
				hashedinput = hashlib.sha256(hashinput.encode('utf-8')).hexdigest()
				hashkey = str(hashedinput[0:16])
				Accepted.objects.create(
					lid=offer.lid,
					oid=offer.oid,
					lamount=offer.lamount*Decimal((1-(postcollected/100))),
					oamount=offer.oamount*Decimal((1-(offercollected/100))),
					postpartner_receiving=offer.postpartner_receiving,
					offerpartner_receiving=offer.offerpartner_receiving,
					u1=offer.u1,
					u2=offer.u2,
					u3=offer.u3,
					u4=offer.u4,
					hashkey=hashkey
				)
				post.amount = offer.lid.amount - offer.lamount
				otheritem.amount = offer.oid.amount - offer.oamount
				post.save()
				otheritem.save()
				offer.delete()

			# Offer rejected
			elif request.POST.get('response') == 'option 2':
				offer.delete()
			return redirect("/listings/mylistings")
		if 'submit_counter' in request.POST:
			if form2.is_valid():
				counter = form2.save(commit=False)
				if offer.lastsent%2: #if post party is counteroffering
					offer.postpartner_receiving=counter.offerpartner_receiving
					offer.lid=counter.oid
				else: #if other party is counteroffering
					offer.offerpartner_receiving=counter.offerpartner_receiving
					offer.oid=counter.oid
				offer.lamount=counter.lamount
				offer.oamount=counter.oamount
				offer.lastsent = offer.lastsent+1
				offer.save()
				return redirect("".join(["/listings/",str(offer.lid.id),"/",str(offer.oid.id),"/offer"]))

	template = loader.get_template("listings/offerdetails.html")
	context = {"post": post,
			"offer": offer,
			"otheritem": otheritem,
			"curr": curr,
			"form": form,
			"form2": form2,
			"offercollected": offercollected,
			"postcollected": postcollected}
	return HttpResponse(template.render(context, request))

def accepted_details(request, pid, oid):
    post = Listing.objects.get(id=pid)
    otheritem = Listing.objects.get(id=oid)
    trade = Accepted.objects.get(lid=pid,oid=oid)
    form = HashVerificationForm(request.POST or None)
    curr = request.user
    hashkey = None
    thisuserverified = False
    tradecomplete = False
    ver = 0
    if post.user.id==curr.id:
        hashkey = trade.hashkey[:8]
        ver = 1
    if otheritem.user.id==curr.id:
        hashkey = trade.hashkey[8:]
        ver = 2
    if trade.verified==ver:
        thisuserverified = True
    if curr.profile.partner:
        if post.user.id==curr.profile.partner.id and ver==1:
            thisuserverified = True
        if otheritem.user.id==curr.profile.partner.id and ver==2:
            thisuserverified = True
    if trade.verified==3:
        tradecomplete = True
	
    if request.method == 'POST':
        if form.is_valid():
            if request.POST.get('hashver')==hashkey:
                if trade.verified+ver==3:
                    trade.verified=3
                else:	
                    trade.verified=ver
                trade.save()
                return redirect("".join(["/listings/",str(pid),"/",str(oid),"/accepted"]))

    template = loader.get_template("listings/accepteddetails.html")
    context = {
        "post": post,
        "otheritem": otheritem,
        "trade": trade,
        "form": form,
        "hashkey": hashkey,
		"ver": thisuserverified,
		"complete": tradecomplete,
    }
    return HttpResponse(template.render(context, request))

def test(request, teststr):
	template = loader.get_template("listings/test.html")
	context = {"teststr":teststr}
	return HttpResponse(template.render(context,request))