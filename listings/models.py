from django.db import models

# Create your models here.
class Listing(models.Model):
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    img_link = models.CharField(max_length=100)
