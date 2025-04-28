from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'Overview/home.html'

class PenTView(TemplateView):
    template_name = 'Overview/PenT.html'

class WebView(TemplateView):
    template_name = 'Overview/Web.html'

class ArduinoView(TemplateView):
    template_name = 'Overview/arduino.html'

class PFUView(TemplateView):
    template_name = 'Overview/PowerFromUndergroundhtml'

class ACCTView(TemplateView):
    template_name = 'Overview/ACCTT.html'

class EducationView(TemplateView):
    template_name = 'Overview/Education.html'

class CareerView(TemplateView):
    template_name = 'Overview/Career.html'

class HTMLView(TemplateView):
    template_name = 'Overview/bootstrapexamples.html'

