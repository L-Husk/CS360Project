from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm, SetPartnerForm, RemovePartnerForm
from django.contrib.auth.models import User
from listings.models import PartnerRequest, Profile

# Create your views here.
def registration_view(request):
	if request.method=="POST": #after submitting registration
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			if user.is_authenticated:
				return redirect("/listings/")
	#registering user
	form = UserForm()
	template = loader.get_template("users/register.html")
	context = {"form":form}
	return HttpResponse(template.render(context, request))

def login_view(request):
	if request.method=="POST": #after signing in
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			if request.user.is_superuser:
				return redirect("/admin")
			return redirect("/listings/")    
	form = AuthenticationForm()
	template = loader.get_template("users/login.html")
	context = {"form": form}
	return HttpResponse(template.render(context, request))

def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('/listings/')

def profile_details(request):
	prof = request.user
	form = SetPartnerForm(request.POST or None)
	removeform = RemovePartnerForm(request.POST or None)
	if request.method=='POST':
		if 'submit_add' in request.POST and form.is_valid():
			obj = form.save(commit=False)
			if PartnerRequest.objects.filter(inputuser=prof.id):
				req = PartnerRequest.objects.get(inputuser=prof.id)
				req.email=obj.email
				if prof.email!=obj.email:
					req.save()
			else:
				obj.inputuser=prof.id
				if prof.email!=obj.email:
					obj.save()
			partner = User.objects.filter(email=obj.email)
			if partner:
				p = User.objects.get(email=obj.email)
				preq = PartnerRequest.objects.filter(inputuser=p.id)
				if preq: #checks if the user they requested has made a partner request
					preq = PartnerRequest.objects.get(inputuser=p.id)
					if preq.email==prof.email:
						thispartner = Profile.objects.get(user_id=prof.id)
						thatpartner = Profile.objects.get(user_id=p.id)
						thispartner.partner_id=p.id
						thatpartner.partner_id=prof.id
						thispartner.save()
						thatpartner.save()
						thisreq = PartnerRequest.objects.get(inputuser=prof.id)
						thatreq = PartnerRequest.objects.get(inputuser=p.id)
						thisreq.delete()
						thatreq.delete()
		if 'submit_remove' in request.POST and removeform.is_valid():
			curr = request.user
			rmreq = removeform.cleaned_data['name']
			if rmreq==curr.username:
				thisprofile = Profile.objects.get(user_id=curr.id)
				thatprofile = Profile.objects.get(user_id=thisprofile.partner_id)
				thisprofile.partner_id = None
				thatprofile.partner_id = None
				thisprofile.save()
				thatprofile.save()


	if request.user.is_authenticated:
		curr = request.user
		pend = PartnerRequest.objects.filter(inputuser=curr.id)
		if pend:
			pend = PartnerRequest.objects.get(inputuser=curr.id)
		context = {"form": form,
			 "removeform": removeform,
			 "pend": pend}
		template = loader.get_template("users/profile.html")
		return HttpResponse(template.render(context, request))
		#make the actual page when done
	else:
		return redirect("/users/login")