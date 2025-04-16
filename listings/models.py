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
	user = models.ForeignKey(User, default=1, null=True,on_delete=models.SET_NULL)
	def __str__(self):
		return self.item_name
	
class Pending(models.Model):
	lid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listed')
	oid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offered')
	lamount = models.IntegerField()
	oamount = models.IntegerField()
	u1 = models.IntegerField(null=True, blank=True) #poster
	u2 = models.IntegerField(null=True, blank=True) #poster's partner
	u3 = models.IntegerField(null=True, blank=True) #responder
	u4 = models.IntegerField(null=True, blank=True) #responder's partner
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	partner = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='partner')
	
	def __str__(self):
		return self.user.username
	
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
#adds a profile for each new user
post_save.connect(create_profile, sender=User)