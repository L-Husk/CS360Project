from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

# Create your models here.
class Listing(models.Model):
	item_name = models.CharField(max_length=100)
	item_desc = models.CharField(max_length=500)
	pub_date = models.DateTimeField(auto_now_add = True)
	img = models.ImageField(default='default.jpg', blank=True)
	user = models.ForeignKey(User, default=1, null=True,on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=20, decimal_places=3)
	is_alive = models.BooleanField(default=False) #adds 5% to handling cost
	is_chilled = models.BooleanField(default=False) #adds 3% to handling cost
	is_fragile = models.BooleanField(default=False) #adds 2% to handling cost
	def __str__(self):
		return self.item_name
	
class Pending(models.Model):
	lid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listed')
	oid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offered')
	lamount = models.DecimalField(max_digits=20, decimal_places=3)
	oamount = models.DecimalField(max_digits=20, decimal_places=3)
	class sendchoice(models.TextChoices):
		Myself = 'Myself'
		My_Partner = 'My Partner'
	postpartner_receiving = models.CharField(max_length=50, choices=sendchoice.choices) #this selects whether the person who posted the item is receiving the offered item, or their partner
	offerpartner_receiving = models.CharField(max_length=50, choices=sendchoice.choices) #this selects whether the person making an offer has the item, or their partner
	u1 = models.IntegerField(null=True, blank=True) #poster
	u2 = models.IntegerField(null=True, blank=True) #poster's partner
	u3 = models.IntegerField(null=True, blank=True) #responder
	u4 = models.IntegerField(null=True, blank=True) #responder's partner
	lastsent = models.IntegerField(default=1) # %%2=0 is the original party, %%2=1 is the party that responded. Anything > 1 is a counteroffer
	accepted = models.BooleanField(default=False) #true denotes a finished offer

class Accepted(models.Model):
	lid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='accepted_listed')
	oid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='accepted_offered')
	lamount = models.DecimalField(max_digits=20, decimal_places=3)
	oamount = models.DecimalField(max_digits=20, decimal_places=3)
	class sendchoice(models.TextChoices):
		Myself = 'Myself'
		My_Partner = 'My Partner'
	postpartner_receiving = models.CharField(max_length=50, choices=sendchoice.choices) #this selects whether the person who posted the item is receiving the offered item, or their partner
	offerpartner_receiving = models.CharField(max_length=50, choices=sendchoice.choices) #this selects whether the person making an offer has the item, or their partner
	u1 = models.IntegerField(null=True, blank=True) #poster
	u2 = models.IntegerField(null=True, blank=True) #poster's partner
	u3 = models.IntegerField(null=True, blank=True) #responder
	u4 = models.IntegerField(null=True, blank=True)
	completed_at = models.DateTimeField(auto_now_add=True)
	verified = models.IntegerField(default=0)
	hashkey = models.CharField(max_length=16, null=True, blank=True)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	partner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='partner')
	
	def __str__(self):
		return self.user.username
	
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
#adds a profile for each new user
post_save.connect(create_profile, sender=User)

class PartnerRequest(models.Model):
	email = models.EmailField()
	inputuser = models.IntegerField(blank=True, null=True)
	def __str__(self):
		return self.email
	