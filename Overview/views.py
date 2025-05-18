from django.shortcuts import render
from django.views.generic import TemplateView
from sympy.physics.units import temperature

from Overview.forms import FlashInputForm,BinaryInputForm
from Overview.PowerFromUnderground.SimpleFlashCycle import FlashCycle
from Overview.PowerFromUnderground.SimpleBinaryCycle import SimpleBinary
from Overview.PowerFromUnderground.linspace import linspace
from Overview.PowerFromUnderground import coolprop_fluids

from CoolProp.CoolProp import PropsSI


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

class PFUView(TemplateView):
    template_name = 'Overview/PowerFromUnderground.html'

def portfolio(request):
    projects = Project.objects.all()
    return render(request, 'Overview/portfolio.html', {'projects': projects})

def plot_flash(request):
    form = FlashInputForm()
    para_work_out_array = []
    percentage_array = []
    output = {
        'Work_out': 0,
        'heat_out': 0,
        'state_entropies': [],
        'state_temperatures': [],
        'S_liq': [],
        'S_vap': [],
        'temperature_range':[]}
    dP = 0

    if request.method == 'POST':
        form = FlashInputForm(request.POST)
        if form.is_valid():
            m_dot = form.cleaned_data['mass_flow_rate']
            T1 = form.cleaned_data['init_temp']
            T2 = form.cleaned_data['final_temp']
            P1 = form.cleaned_data['init_pressure']
            dP = form.cleaned_data['pressure_change']

            try:
                # Base run for plotting
                output = FlashCycle(
                    m_dot, init_temp=T1, final_temp=T2, init_pressure=P1,
                    pressure_change=(dP/100), PropsSI=PropsSI, linspace=linspace
                )

                # Parametric analysis
                percentage_array = [x / 1000 for x in range(10, 950, 25)]

                for i in percentage_array:
                    para_output = FlashCycle(
                        m_dot, init_temp=T1, final_temp=T2, init_pressure=P1,
                        pressure_change=i, PropsSI=PropsSI, linspace=linspace
                    )
                    para_work_out_array.append(para_output["Work_out"] * -1)
                    print(para_work_out_array)
            except Exception as error:
                form.add_error(None, error)

    return render(request, 'Overview/flash_cycle_plot.html', {
        'form': form, 'pressure_change':dP,
        'Entropies': json.dumps(output["state_entropies"]),
        'Temperatures': json.dumps(output["state_temperatures"]),
        'Sliq': json.dumps(output["S_liq"]),
        'Svap': json.dumps(output["S_vap"]),
        'range': json.dumps(output["temperature_range"]),
        'para_work_out_array': json.dumps(para_work_out_array),
        'percentage_array': json.dumps(percentage_array)
    })

def plot_binary(request):
    form  = BinaryInputForm()
    output = {
        'state_enthalpies': [],
        'state_pressures': [],
        'state_entropies': [],
        'state_temperatures' : [],
        'saturation_dome': []
    }


    if request.method == 'POST':
        form = BinaryInputForm(request.POST)
        if form.is_valid():
            working_fluid = form.cleaned_data['working_fluid']
            m_geo_dot = form.cleaned_data['mass_flow_rate']
            production_well_temperature = form.cleaned_data['production_well_temperature']
            injection_well_temperature = form.cleaned_data['injection_well_temperature']
            suerheat = form.cleaned_data['superheat']
            turbine_inlet_pressure =  form.cleaned_data['turbine_inlet_pressure']
            condenser_outlet_temperature = form.cleaned_data['condenser_outlet_temperature']

            try:
                output = SimpleBinary(working_fluid, m_geo_dot, [production_well_temperature, injection_well_temperature], suerheat, turbine_inlet_pressure, condenser_outlet_temperature,PropsSI)

            except Exception as error:
                form.add_error(None, error)


    return render(request, 'Overview/binary_cycle_plot.html', {'form':form, 'Enthalpies': json.dumps(output['state_enthalpies']), 'Pressures': json.dumps(output['state_pressures']),
                                                                   'Entropies': json.dumps(output['state_entropies']), 'Temperatures': json.dumps(output['state_temperatures']),
                                                               'saturation_dome': json.dumps(output['saturation_dome'])})


def comparison_table(request):
    return render(request, 'Overview/WorkingFluid.html', {'fluids': coolprop_fluids})


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

