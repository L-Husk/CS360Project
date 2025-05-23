from django import forms
from .models import Listing
from .models import Pending
from .models import PartnerRequest

class UserForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'item_desc','amount','img','is_alive','is_chilled','is_fragile']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Pending
        fields = ['oid', 'lamount', 'oamount', 'offerpartner_receiving']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        partner = kwargs.pop('partner', None)  
        super().__init__(*args, **kwargs)

        if user:
            qs = Listing.objects.filter(user=user)
            if partner:
                qs = qs | Listing.objects.filter(user=partner)
            qs = qs.exclude(amount=0)
            self.fields['oid'].queryset = qs.distinct()

class OfferResponseForm(forms.Form):
    response = forms.ChoiceField(choices=[('option 1', 'Accept'), ('option 2', 'Reject')], widget=forms.RadioSelect)
    sendchoice = [
        ('Myself', 'Myself'),
        ('My_Partner', 'My Partner')
    ]
    partner_receiving = forms.ChoiceField(choices=sendchoice)
    
class HashVerificationForm(forms.Form):
    hashver = forms.CharField(max_length=20)