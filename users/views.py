from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm

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
			return redirect("listings/")
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
	if request.user.is_authenticated:
		context = {}
		template = loader.get_template("users/profile.html")
		return HttpResponse(template.render(context, request))
		#make the actual page when done
	else:
		return redirect("/users/login")