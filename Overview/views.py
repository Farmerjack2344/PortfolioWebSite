from django.shortcuts import render
from django.views.generic import TemplateView
from sympy.physics.units import temperature
from django.http import JsonResponse

from Overview.forms import FlashInputForm,BinaryInputForm
from Overview.PowerFromUnderground.SimpleFlashCycle import FlashCycle
from Overview.PowerFromUnderground.SimpleBinaryCycle import SimpleBinary,simple_binary_parametric
from Overview.PowerFromUnderground.linspace import linspace
from Overview.PowerFromUnderground.coolprop_fluids import coolprop_fluids, property_generator

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
        'saturation_dome': [],
        'Work_out': 0,  
        'Work_in': 0,   
        'Heat_out': 0,
    }
    para_work_out_array = []
    T_range = []    
    P_range = []

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
                output = SimpleBinary(working_fluid, m_geo_dot, [production_well_temperature, injection_well_temperature], 
                                      suerheat, turbine_inlet_pressure, condenser_outlet_temperature,PropsSI)
            except Exception as error:
                form.add_error(None, error)

            

    return render(request, 'Overview/binary_cycle_plot.html', {'form':form, 'Enthalpies': json.dumps(output['state_enthalpies']), 'Pressures': json.dumps(output['state_pressures']),
                                                                   'Entropies': json.dumps(output['state_entropies']), 'Temperatures': json.dumps(output['state_temperatures']),
                                                               'saturation_dome': json.dumps(output['saturation_dome']),'Work_out': output['Work_out'], 'Work_in': output['Work_in'],
                                                                 'Heat_out': output['Heat_out']})

def load_parametric(request):
    if request.method == 'GET':
        working_fluid = request.GET.get('working_fluid')
        m_dot_geo_fluid = request.GET.get('mass_flow_rate')
        reservoir = [float(request.GET.get('production_well_temperature')), float(request.GET.get('injection_well_temperature'))]
        superheat = request.GET.get('superheat')
        turbine_in_pressure = request.GET.get('turbine_inlet_pressure')
        condenser_out_temperature = request.GET.get('condenser_outlet_temperature')

        para_work_out_array = []
        T_range = []
        P_range = []

        try:
            para_work_out_array = simple_binary_parametric(working_fluid, m_dot_geo_fluid, reservoir, superheat, turbine_in_pressure, condenser_out_temperature, PropsSI)


            return JsonResponse({
                'para_work_out_array': para_work_out_array,
                'T_range': T_range,
                'P_range': P_range,
            })
            
        except Exception as error:
            print(error)#remove this line when done
            return JsonResponse({'error': str(error)}, status=500)


        return json.dumps(para_work_out_array)

def comparison_table(request):
    # This function is used to create a comparison table for the fluids
    fluid_properties = []
    selected_fluids = []
    human_name = []
    flag = 0
    if request.method == 'POST':
        selected_fluids = request.POST.getlist('fluids')#This gets the CoolProp Input from the Checkbox
        
        selected_fluids = [x.upper() for x in selected_fluids]#Most cool prop inputs are uppercase
        try:
            for alias, human in coolprop_fluids:# The check box only return the alias name, so we need to get the human name
                

                if (alias.upper() in selected_fluids): #This finds the alias in the selected fluids
                    human_name.append(human)
                    print(human)
            
            
            for fluid in property_generator(selected_fluids, PropsSI):
                fluid.insert(0, human_name[flag])#This adds the human name to the beginning of the fluid proprties list
                flag += 1
                fluid_properties.append(fluid)#This adds the fluid properties to the list
        except Exception as error:
            pass
            

    return render(request, 'Overview/WorkingFluid.html', {'fluids': coolprop_fluids, 'selected_fluids': selected_fluids, 'human_name': human_name, 'fluid_properties': fluid_properties})


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

