from django.shortcuts import render
from django.views.generic import TemplateView
from sympy.physics.units import temperature

from Overview.forms import FlashInputForm
from Overview.PowerFromUnderground.SimpleFlashCycle import FlashCycle
from CoolProp.CoolProp import PropsSI
from Overview.PowerFromUnderground.linspace import linspace
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

class PFUView(TemplateView):
    template_name = 'Overview/PowerFromUnderground.html'

def plot_flash(request):
    #FlashCycle(419, 250, 48.5671, 3972.06e3, (650e3 / 3972.06e3))
    form = FlashInputForm()
    state_temperatures = []# This will hold the temperature from the flash cycle
    state_entropies = []# This will hold the entropies from the flash cycle
    S_liq = []
    S_vap = []
    temperature_range = []
    if request.method == 'POST':
        form  = FlashInputForm(request.POST)
        if form.is_valid():
            m_dot = form.cleaned_data['mass_flow_rate']
            T1 = form.cleaned_data['init_temp']
            T2 = form.cleaned_data['final_temp']
            P1 = form.cleaned_data['init_pressure']
            dP = form.cleaned_data['pressure_change']
            try:

                Work_out, heat_out, state_entropies, state_temperatures, efficiency, pressure_change, S_liq, S_vap, temperature_range\
                    = FlashCycle(m_dot, init_temp = T1, final_temp = T2, init_pressure = P1, pressure_change = dP, PropsSI=PropsSI, linspace = linspace)

            except Exception as error:
                form.add_error(None, error)
                print(error)


    else:
        form = FlashInputForm()

    return render(request, 'Overview/flash_cycle_plot.html', {'form': form,'Entropies': json.dumps(state_entropies),'Temperatures': json.dumps(state_temperatures), 'Sliq': json.dumps(S_liq), 'Svap': json.dumps(S_vap), 'range': json.dumps(temperature_range)})

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

