from django.db import models

# Create your models here.
class PartnerRequest(models.Model):
	email = models.EmailField(unique=True)
	inputuser = models.IntegerField()
	def __str__(self):
		return self.email