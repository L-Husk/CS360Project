from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm, SetPartnerForm
from django.contrib.auth.models import User
from listings.models import PartnerRequest

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
	if request.method=='POST':
		if form.is_valid():
			obj = form.save(commit=False)
			obj.inputuser=prof.id
			obj.save()
			partner = User.objects.filter(email=obj.email)
			if partner:
				p = User.objects.get(email=obj.email)
				preq = PartnerRequest.objects.filter(inputuser=p.id)
				if preq: #buncha if-else statements that do nothing
					#currently, preq returns none even if it shouldn't
					return redirect("/listings/")
				else:
					''
					#return redirect("/listings/mylistings")
			

	if request.user.is_authenticated:
		curr = request.user
		pend = PartnerRequest.objects.all()#filter(inputuser=curr.id)
		if pend:
			#pend = PartnerRequest.objects.get(inputuser=curr.id)
			pend = None
		context = {"form": form,
			 "pend": pend}
		template = loader.get_template("users/profile.html")
		return HttpResponse(template.render(context, request))
		#make the actual page when done
	else:
		return redirect("/users/login")