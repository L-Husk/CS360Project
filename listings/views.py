from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question

# Create your views here.
def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("listings/index.html")
    context = {"latest_questions": latest_questions}
    return HttpResponse(template.render(context, request))