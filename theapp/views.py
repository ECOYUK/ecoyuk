from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.

class HelloBrehs(TemplateView):
    template_name = "templates/mdhomepage.html"










