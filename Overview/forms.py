from cProfile import label
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import FloatField
from Overview.PowerFromUnderground.coolprop_fluids import coolprop_fluids

import CoolProp

def validate_working_fluid(value):
    if value not in CoolProp.__fluids__:
        raise ValidationError("This fluid is not within the CoolProp database")



class FlashInputForm(forms.Form):
    mass_flow_rate = forms.FloatField(label="Mass Flow Rate (kg/s):")
    init_temp = forms.FloatField(label="Initial Temperature(°C):")
    final_temp = forms.FloatField(label="Final Temperature (°C):")
    init_pressure = forms.FloatField(label="Initial Pressure (Pa):")
    pressure_change = forms.FloatField(label="Pressure Change (%):")


class BinaryInputForm(forms.Form):
    working_fluid = forms.CharField(label="Working Fluid:", max_length=100)
    mass_flow_rate = forms.FloatField(label="Mass Flow Rate of geo fluid (kg/s):")
    production_well_temperature = forms.FloatField(label="Temperature at the production well  (K):")
    injection_well_temperature = forms.FloatField(label="Temperature at the injection well (K):")
    superheat = forms.FloatField(label="Superheat (K):")
    turbine_inlet_pressure = forms.FloatField(label="Turbine Inlet Pressure (Pa):")
    condenser_outlet_temperature = forms.FloatField(label="Condenser Outlet Temperature (K):")
    
