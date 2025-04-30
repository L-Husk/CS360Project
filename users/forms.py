from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from listings.models import PartnerRequest, Profile

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )

class SetPartnerForm(forms.ModelForm):
    class Meta:
        model = PartnerRequest
        fields = ['email']

class RemovePartnerForm(forms.Form):
    name = forms.CharField(label="username",max_length=200)