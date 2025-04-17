from django import forms
from .models import Listing
from .models import Pending

class UserForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'item_desc','amount','img']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Pending
        fields = ['oid', 'lamount', 'oamount']