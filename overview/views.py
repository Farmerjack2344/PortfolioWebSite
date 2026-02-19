from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse



from CoolProp.CoolProp import PropsSI # type: ignore


from .models import Project
import json

# Create your views here.
class HomeView(TemplateView):
    template_name = 'Overview/home.html'

class PenTView(TemplateView):
    template_name = 'Overview/PenT.html'

class WebView(TemplateView):
    template_name = 'Overview/Web.html'

class ArduinoView(TemplateView):
    template_name = 'Overview/arduino.html'

def portfolio(request):
    projects = Project.objects.all()
    return render(request, 'Overview/portfolio.html', {'projects': projects})


class ACCTView(TemplateView):
    template_name = 'Overview/ACCTT.html'

class EducationView(TemplateView):
    template_name = 'Overview/Education.html'

class CareerView(TemplateView):
    template_name = 'Overview/Career.html'

class CVView(TemplateView):
    template_name = 'Overview/CV.html'

class HTMLView(TemplateView):
    template_name = 'Overview/bootstrapexamples.html'

