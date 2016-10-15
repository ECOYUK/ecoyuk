from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.

class HelloBrehs(TemplateView):
    template_name = "templates/mdhomepage.html"


class About(TemplateView):
    template_name = "templates/aboutpage.html"


class Contact(TemplateView):
    template_name = "templates/contactpage.html"
