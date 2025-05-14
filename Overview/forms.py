from django import forms

class FlashInputForm(forms.Form):
    mass_flow_rate = forms.FloatField(label="Mass Flow Rate:")
    init_temp = forms.FloatField(label="Initial Temperature:")
    final_temp = forms.FloatField(label="Final Temperature:")
    init_pressure = forms.FloatField(label="Initial Pressure:")
    pressure_change = forms.FloatField(label="Pressure Change:")
