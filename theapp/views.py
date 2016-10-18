from django.views.generic import TemplateView, ListView, DetailView
from .models import *


class HelloBrehs(TemplateView):
    template_name = "templates/mdhomepage.html"


class About(TemplateView):
    template_name = "templates/aboutpage.html"


class Contact(TemplateView):
    template_name = "templates/contactpage.html"


class InfoListView(ListView):
    model = InfoModel
    template_name = "templates/infomodel_list.html"


class InfoDetailView(DetailView):
    model = InfoModel
    template_name = "templates/infomodel_detail.html"
