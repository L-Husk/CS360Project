from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def registration_view(request):
    if request.method=="POST": #after submitting registration
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/users/login")
    #registering user
    form = UserCreationForm()
    template = loader.get_template("users/register.html")
    context = {"form":form}
    return HttpResponse(template.render(context, request))

def login_view(request):
    if request.method=="POST": #after signing in
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/listings")    
    form = AuthenticationForm()
    template = loader.get_template("users/login.html")
    context = {"form": form}
    return HttpResponse(template.render(context, request))