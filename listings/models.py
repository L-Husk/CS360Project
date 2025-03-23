from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text

class Ans(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Listing(models.Model):
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    img_link = models.CharField(max_length=100)
