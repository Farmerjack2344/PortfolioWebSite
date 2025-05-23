from django.shortcuts import render
from PowerFromUndergroundApp.forms import FlashInputForm,BinaryInputForm
from PowerFromUndergroundApp.PowerFromUnderground.SimpleFlashCycle import FlashCycle
from PowerFromUndergroundApp.PowerFromUnderground.SimpleBinaryCycle import SimpleBinary, simple_binary_parametric, SimpleBinary, SimpleBinaryGenerator
from PowerFromUndergroundApp.PowerFromUnderground.linspace import linspace
from PowerFromUndergroundApp.PowerFromUnderground.coolprop_fluids import coolprop_fluids, property_generator
from django.http import JsonResponse
import json
import numpy as np
from CoolProp.CoolProp import PropsSI # type: ignore
from django.views.generic import TemplateView

# Create your views here.

class PFUView(TemplateView):
    template_name = 'PowerFromUndergroundApp/PowerFromUnderground.html'

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

    return render(request, 'PowerFromUndergroundApp/flash_cycle_plot.html', {
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
        'HeatSinkSource': [],
    }
    para_work_out_array = np.array([])
    T_range = np.array([])
    P_range = np.array([])
    fluid_properties = []
    selected_fluids = []
    human_name = []
    working_fluid_work_outputs = []

    data_points = 20

    if request.method == 'POST':
        form = BinaryInputForm(request.POST)
        if form.is_valid():
            working_fluid = form.cleaned_data['working_fluid']
            m_geo_dot = form.cleaned_data['mass_flow_rate']
            production_well_temperature = form.cleaned_data['production_well_temperature']
            injection_well_temperature = form.cleaned_data['injection_well_temperature']
            superheat = form.cleaned_data['superheat']
            turbine_inlet_pressure =  form.cleaned_data['turbine_inlet_pressure']
            condenser_outlet_temperature = form.cleaned_data['condenser_outlet_temperature']
            data_points = form.cleaned_data['data_points']

            para_work_out_array = np.array([])
            T_range = np.array([])
            P_range = np.array([])
            HeatSinkSource = []
            

            

            try:
                output = SimpleBinary(working_fluid, m_geo_dot, [production_well_temperature, injection_well_temperature], 
                                      superheat, turbine_inlet_pressure, condenser_outlet_temperature,PropsSI)
            except Exception as error:
                form.add_error(None, error)

            try:
                
                for j, i, temperature, pressure, net_work in simple_binary_parametric(working_fluid, m_geo_dot, [production_well_temperature, injection_well_temperature], superheat, turbine_inlet_pressure, condenser_outlet_temperature,data_points, PropsSI):
                    # Process each result as it is generated
                    para_work_out_array = np.append(para_work_out_array, net_work)
                    T_range = np.append(T_range, temperature)
                    P_range = np.append(P_range, pressure)
            except Exception as error:
               
                form.add_error(None, error)

            try:
                selected_fluids = request.POST.getlist('fluids')#This gets the CoolProp Input from the Checkbox
        
                selected_fluids = [x.upper() for x in selected_fluids]#Most cool prop inputs are uppercase
                for selected_fluid in selected_fluids:
                    
                    for working_fluid_work_output in SimpleBinaryGenerator(selected_fluid, m_geo_dot, [production_well_temperature, injection_well_temperature], superheat, turbine_inlet_pressure, condenser_outlet_temperature, PropsSI):
                        working_fluid_work_outputs.append((working_fluid_work_output))

                selected_fluids = [x.lower() for x in selected_fluids]

            except Exception as error:
                form.add_error(None, error)
                print(selected_fluids)
                print(working_fluid_work_outputs)


    return render(request, 'PowerFromUndergroundApp/binary_cycle_plot.html', {'form':form,
                                                                              'Enthalpies': json.dumps(output['state_enthalpies']), 'Pressures': json.dumps(output['state_pressures']),
                                                                              'Entropies': json.dumps(output['state_entropies']), 'Temperatures': json.dumps(output['state_temperatures']),
                                                                              'saturation_dome': json.dumps(output['saturation_dome']),'Work_out': output['Work_out'], 'Work_in': output['Work_in'],
                                                                              'Heat_out': output['Heat_out'], 'HeatSinkSource': json.dumps(output['HeatSinkSource']),
                                                                              'para_work_out_array': para_work_out_array.tolist(), 'T_range': T_range.tolist(),
                                                                              'P_range': P_range.tolist(),'fluids': coolprop_fluids,'working_fluid_work_outputs': working_fluid_work_outputs,
                                                                              'selected_fluids': selected_fluids
                                                                              })



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
            

    return render(request, 'PowerFromUndergroundApp/WorkingFluid.html', {'fluids': coolprop_fluids, 'selected_fluids': selected_fluids, 'human_name': human_name, 'fluid_properties': fluid_properties})

