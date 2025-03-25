from django import forms
from .models import Listing

class UserForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'item_desc','img']